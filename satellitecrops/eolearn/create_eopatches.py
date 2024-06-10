### EO-Learn / SentinelHub ###
from sentinelhub import BBox, BBoxSplitter
from eolearn.core import (
    EOPatch
    )

import geojson
import rasterio
import os

from colorama import Fore, Style


def get_zone_to_patch(bucket):
    '''Retrieve zone to patch from bucket'''
    print(Fore.MAGENTA + "\n⏳ Loading department zone" + Style.RESET_ALL)
    result = bucket.get_blob("contour_zone.geojson")
    geojson_data = geojson.loads(result)
    print(f"✅ Departement zone loaded")
    return gpd.GeoDataFrame(geometry=[geojson_data["geometry"]], crs=4326)

def create_bbox_of_zone(zone, resolution=10, patch_dim=256):
    '''Create bounding boxes that cover the zone'''
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

def get_sat_image(bucket, bands=1):
    '''Retrieve sat image from bucket'''
    print(Fore.MAGENTA + "\n⏳ Loading satellite image of the zone" + Style.RESET_ALL)
    file_path = os.path.join(DATA_PATH, "out_image.jp2")
    with rasterio.open(file_path) as mosaic_data:
        sat_bounds = mosaic_data.bounds
        sat_image = mosaic_data.read()
    print(f"✅ Satellite image loaded")
    return sat_bounds, sat_image

def create_sat_eopatch(sat_bounds, sat_image):
    '''Create one big eopatch for the whole sat image'''
    sat_patch = EOPatch(bbox=BBox(bbox=sat_bounds, crs=LOCAL_CRS))
    if sat_image.ndim == 3:
        sat_patch.data_timeless["BANDS"] = sat_image
    else:
        sat_patch.data_timeless['BANDS'] = sat_image[..., np.newaxis]
    return sat_patch

def zone2sat_patch(bucket):
    sat_bounds, sat_image = get_sat_image(bucket, 3)
    sat_patch = create_sat_eopatch(sat_bounds, sat_image)
    return sat_patch


def get_parcelles_from_db(zone):
    print(Fore.MAGENTA + "\n⏳ Getting parcelles infos" + Style.RESET_ALL)
    parcelles_path = os.path.join(DATA_PATH, f"{DPT}_parcelles.geojson")

    if not os.path.isfile(parcelles_path):
        conn = SQLConnection()
        parcelles_df = conn.get_parcelles_in_bbox(zone.geometry, 2154)
        parcelles_df["code_group"] = parcelles_df.code_group.astype("int64")
        parcelles_df.to_file(parcelles_path)
    print(f"✅ Parcelles loaded locally")
    return parcelles_path
