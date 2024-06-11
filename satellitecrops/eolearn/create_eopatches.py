### EO-Learn / SentinelHub ###
from sentinelhub import BBox, BBoxSplitter
from eolearn.core import (
    EOPatch
    )

import geojson
import rasterio
import os
import numpy as np
from params import *

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
    '''Create one eopatch for the whole sat image'''
    sat_patch = EOPatch(bbox=BBox(bbox=sat_bounds, crs=LOCAL_CRS))
    if sat_image.ndim == 3:
        sat_patch.data_timeless["BANDS"] = sat_image
    else:
        sat_patch.data_timeless['BANDS'] = sat_image[..., np.newaxis]
    return sat_patch

def create_sat_eopatches(bucket):
    sat_dir_path = os.path.join(DATA_DIR_LOCAL, SAT_IMG_FOLDER, DPT_FOLDER, IMG_ORIGIN, IMG_LOC, YEAR, "1")
    shots_list = os.listdir(sat_dir_path)
    num_shots = len(shots_list)
    img_clean = np.zeros((1))
    for i in range(num_shots):
        img_path = os.path.join(sat_dir_path, shots_list[i], 'TCI.tif')
        cld_path = os.path.join(sat_dir_path, shots_list[i], 'SCL.tif')
        if os.path.isfile(img_path) & os.path.isfile(cld_path):
            with rasterio.open(img_path) as img_file:
                with rasterio.open(cld_path) as cld_file:
                    img = img_file.read()
                    print(img.shape, img.strides)
                    if img_clean.shape != img.shape:
                        img_clean = np.zeros(img.shape, dtype=np.uint8)
                    cld = np.repeat(np.repeat(np.isin(cld_file.read(), [4, 5, 6, 7]), 2, axis=2), 2, axis=1)
                    img_clean[img_clean==0]= (img*(np.repeat(cld, img.shape[0], axis=0)))[img_clean==0]
                    print(img_clean.shape, img_clean.strides)
    del img
    del cld
#def get_sat_images(bucket, ):

def merge_monthly_sat_bands(month_dir):
    '''Merge all shots of a month for each band
    Shots are filtered by maskcloud (scl: scene classification) and merged
    Parameters:
    month_dir: path to the directory of given month
    Return:
    dict of bands, key are band names and values are merge data'''
    shots_list = os.listdir(month_dir)
    num_shots = len(shots_list)
    bands_merged = {band: np.zeros((1))for band in BANDS_USED}
    for i in range(num_shots):
        cld_path = os.path.join(month_dir, shots_list[i], 'SCL.tif')
        # tranform from shape (1, 5490, 5490) to shape (1, 10980, 10980)
        cld = np.repeat(np.repeat(np.isin(cld_file.read(), [4, 5, 6, 7]), 2, axis=2), 2, axis=1)
        with rasterio.open(cld_path) as cld_file:
            for key, band_merged in bands_merged.items():
                band_path = os.path.join(month_dir, shots_list[i], key+'.tif')
                with rasterio.open(band_path) as band_file:
                    band_data = band_file.read()
                    if key == "B11": # from shape (1, 5490, 5490) to shape (1, 10980, 10980)
                        band_data = np.repeat(np.repeat(band_data, 2, axis=2), 2, axis=1)
                    if band_merged.shape != band_data.shape:
                        band_merged = np.zeros(band_data.shape, dtype=np.uint8)
                    band_merged[band_merged==0]= (band_data*(np.repeat(cld, band_data.shape[0], axis=0)))[band_merged==0]
                bands_merged[key] = band_merged
                del band_data
                del band_merged
        del cld
    return bands_merged

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
