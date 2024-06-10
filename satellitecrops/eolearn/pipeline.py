### Data manipulation ###
import pandas as pd
import numpy as np
import geopandas as gpd
from bs4 import BeautifulSoup
import rasterio
from shapely.geometry import Polygon

### Utils ###
from datetime import datetime
import os
import sys
from satellitecrops.utils.sql_connector import SQLConnection
from satellitecrops.params import *
from satellitecrops.utils.bucket import BucketConnector
import geojson
from colorama import Fore, Style

# from tqdm import tqdm

### Data viz ###
import matplotlib.pyplot as plt
from rasterio.plot import show
from rasterio.merge import merge

### eolearn tools
# from satellitecrops.eolearn.enrich_eopatches import add_sat_patch_to_eopatch

### EO-Learn / SentinelHub ###
from sentinelhub import BBox, CRS, BBoxSplitter, TileSplitter
from eolearn.core import (
    EOPatch,
    EOExecutor,
    FeatureType,
    EOTask,
    SaveTask,
    OverwritePermission,
    EOWorkflow,
    linearly_connect_tasks
    )
from eolearn.io import SentinelHubInputTask, VectorImportTask
from eolearn.geometry import VectorToRasterTask

def init_env():
    print(Fore.MAGENTA + "\n⏳ Init environnement" + Style.RESET_ALL)
    for folder in (EOPATCH_FOLDER, EOPATCH_SAMPLES_FOLDER, RESULTS_FOLDER):
        os.makedirs(folder, exist_ok=True)
    print(f"✅ Environnement loaded")


def get_img_coordinates(path):
    with open(os.path.join(path, "metadata.xml")) as fd:
        soup = BeautifulSoup(fd, "xml")
        zone_coordinate = soup.find("EXT_POS_LIST").text.split()
        zone_coordinate = np.array(zone_coordinate).reshape(
            int(len(zone_coordinate)/2), 2
        )
        return zone_coordinate


def get_zone_to_patch(bucket):
    print(Fore.MAGENTA + "\n⏳ Loading department zone" + Style.RESET_ALL)
    result = bucket.get_blob("contour_zone.geojson")
    geojson_data = geojson.loads(result)
    print(f"✅ Departement zone loaded")
    return gpd.GeoDataFrame(geometry=[geojson_data["geometry"]], crs=4326)

def get_sat_image(bucket, bands=1):
    print(Fore.MAGENTA + "\n⏳ Loading satellite image of the zone" + Style.RESET_ALL)
    file_path = os.path.join(DATA_PATH, "out_image.jp2")
    with rasterio.open(file_path) as mosaic_data:
        sat_bounds = mosaic_data.bounds
        sat_image = mosaic_data.read()
    print(f"✅ Satellite image loaded")
    return sat_bounds, sat_image

def create_bbox_of_zone(zone, resolution=10, patch_dim=256):
    print(Fore.MAGENTA + "\n⏳ Creating BBox of the departement" + Style.RESET_ALL)
    splitter = BBoxSplitter(
        zone.geometry.values,
        LOCAL_CRS,
        split_size=patch_dim * resolution
    )
    bbox_list = np.array(splitter.get_bbox_list())
    info_list = np.array(splitter.get_info_list())
    print(f"✅ {len(bbox_list)} BBox created on the department")
    return bbox_list, info_list

def create_bbox_gdf(bbox_list, info_list):
    geometry = [Polygon(bbox.get_polygon()) for bbox in bbox_list]

    idxs = [idx for idx, _ in enumerate(info_list)]
    idxs_x = [info["index_x"] for info in info_list]
    idxs_y = [info["index_y"] for info in info_list]

    bbox_gdf = gpd.GeoDataFrame({
        "index": idxs,
        "index_x": idxs_x,
        "index_y": idxs_y}, crs=32630, geometry=geometry)
    return bbox_gdf

def create_sat_eopatch(sat_bounds, sat_image):
    sat_patch = EOPatch(bbox=BBox(bbox=sat_bounds, crs=LOCAL_CRS))
    if sat_image.ndim == 3:
        sat_patch.data_timeless["BANDS"] = sat_image
    else:
        sat_patch.data_timeless['BANDS'] = sat_image[..., np.newaxis]
    return sat_patch

def get_parcelles_from_db(zone):
    print(Fore.MAGENTA + "\n⏳ Getting parcelles infos" + Style.RESET_ALL)
    parcelles_path = os.path.join(DATA_PATH, f"{DPT}_parcelles.geojson")

    if not os.path.isfile(parcelles_path):
        conn = SQLConnection()
        parcelles_df = conn.get_parcelles_in_bbox(zone.geometry, 2154)
        # parcelles_df["code_group"] = parcelles_df.code_group.astype("int64")
        parcelles_df["id_group"] = [0] * len(parcelles_df)
        for code in MAPPING["CODE CULTURE"]:
            parcelles_df.loc[parcelles_df["code_cultu"] == code, 'id_group'] = MAPPING[MAPPING["CODE CULTURE"] == code].id.iloc[0]
        parcelles_df.to_file(parcelles_path)
    print(f"✅ Parcelles loaded locally")
    return parcelles_path

def make_and_run_workflow(parcelles_path, bbox_list, resolution=10):
    print(Fore.MAGENTA + "\n⏳ EO Workflow init and run" + Style.RESET_ALL)
    vector_feature = FeatureType.VECTOR_TIMELESS, "RPG_REFERENCE"

    vector_import_task = VectorImportTask(vector_feature, parcelles_path)

    rasterization_task = VectorToRasterTask(
        vector_feature,
        (FeatureType.MASK_TIMELESS, "MASK"),
        values_column="code_group",
        raster_resolution=resolution,
        raster_dtype=np.uint8
    )

    save = SaveTask(EOPATCH_FOLDER, overwrite_permission=OverwritePermission.OVERWRITE_FEATURES)
    workflow_nodes = linearly_connect_tasks(
        vector_import_task, rasterization_task, save
    )

    workflow = EOWorkflow(workflow_nodes)
    input_node = workflow_nodes[0]
    save_node = workflow_nodes[-1]
    exec_args = []

    for idx, bbox in enumerate(bbox_list):
        exec_args.append(
            {
                input_node: {"bbox": bbox},
                save_node: {"eopatch_folder": f"eopatch_{idx}"}
            }
        )

    executor = EOExecutor(workflow, exec_args, save_logs=True)
    executor.run(workers=None)
    executor.make_report()
    print(f"✅ Workflow Done !")

def add_data2subpatch(sat_patch, eopatch):
    # Find the pixel indices corresponding to the small_bbox
    height, width = sat_patch.data_timeless['BANDS'].shape[-2:]

    min_x, min_y = eopatch.bbox.lower_left
    max_x, max_y = eopatch.bbox.upper_right
    patch_min_x, patch_min_y = sat_patch.bbox.lower_left
    patch_max_x, patch_max_y = sat_patch.bbox.upper_right
    # compute coord of each pixel of sat_patch
    x_pxl_coord = np.linspace(patch_min_x, patch_max_x, width)
    y_pxl_coord = np.linspace(patch_min_y, patch_max_y, height)
    x_min_idx = np.searchsorted(x_pxl_coord, min_x)
    x_max_idx = np.searchsorted(x_pxl_coord, max_x)
    y_min_idx = np.searchsorted(y_pxl_coord, min_y)
    y_max_idx = np.searchsorted(y_pxl_coord, max_y)
    # Copy data features
    new_eopatch = EOPatch(bbox=BBox(bbox=(min_x, min_y, max_x, max_y), crs=LOCAL_CRS))

    for feature_type, feature_name in sat_patch.get_features():
        if feature_type.is_spatial():
            new_eopatch[feature_type][feature_name] = sat_patch[feature_type][feature_name][:,height-y_max_idx:height-y_min_idx, x_min_idx:x_max_idx]
    return new_eopatch

def add_sat_patch_to_eopatch(eopatches_files, sat_patch):
    for eo_file in eopatches_files:
        eo_file_path = os.path.join(EOPATCH_FOLDER, eo_file)
        eopatch = EOPatch.load(eo_file_path, lazy_loading=True)
        new_eopatch = add_data2subpatch(sat_patch, eopatch)
        new_eopatch.save(eo_file_path, overwrite_permission=OverwritePermission.OVERWRITE_FEATURES)
        del eopatch
        del new_eopatch


def main():
    init_env()

    bucket = BucketConnector()

    dpt_zone = get_zone_to_patch(bucket).to_crs(LOCAL_CRS)

    bbox_list, info_list = create_bbox_of_zone(dpt_zone)

    sat_bounds, sat_image = get_sat_image(bucket, 3)

    sat_patch = create_sat_eopatch(sat_bounds, sat_image)

    # bbox_gdf = create_bbox_gdf(bbox_list, info_list)

    parcelles_path = get_parcelles_from_db(dpt_zone)

    make_and_run_workflow(parcelles_path, bbox_list)

    add_sat_patch_to_eopatch(os.listdir(EOPATCH_FOLDER), sat_patch)


if __name__ == "__main__":
    main()
