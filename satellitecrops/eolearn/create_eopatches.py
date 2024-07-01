### EO-Learn / SentinelHub ###
from sentinelhub import BBox, BBoxSplitter
from eolearn.core import (
    EOPatch
    )

import geojson
import json
import rasterio
import os
import numpy as np
from satellitecrops.params import *
import gcsfs
import rasterio

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

def create_sat_eopatch(sat_bounds, sat_image, save=False, file_name=None, dir_path=None, bucket=None):
    '''Create one eopatch for the whole sat image'''
    print(f"eopatch {file_name} creation")
    sat_patch = EOPatch(bbox=BBox(bbox=sat_bounds, crs=LOCAL_CRS))
    sat_patch.data_timeless["BANDS"] = sat_image
    if save:
        bucket.upload_sat_patch(sat_patch, file_name, dir_path)
    else:
        return sat_patch

def retrieve_data_bbox(bucket, begin_of_file_name):
    dir_path = os.path.join(SAT_IMG_FOLDER, DPT_FOLDER, IMG_SOURCE)
    sat_data_properties_file_name = "sat_data_properties.json"
    sat_data_properties_str = bucket.get_blob(sat_data_properties_file_name, dir_path)
    sat_data_properties = json.loads(sat_data_properties_str)
    for key in sat_data_properties.keys():
        if key.startswith(begin_of_file_name):
            return sat_data_properties[key]['bbox']

def create_sat_eopatches(bucket, img_loc, year):
    '''IMG_LOC=30/T/XP
        YEAR=2019'''
    begin_of_file_name="S2B_"+img_loc.replace("/", "")+"_"+str(year)
    bounds=retrieve_data_bbox(bucket, begin_of_file_name)
    for month_num in range(1, 13):
        sat_monthly_dir_path = os.path.join(SAT_IMG_FOLDER, DPT_FOLDER, IMG_SOURCE, IMG_ORIGIN, img_loc, str(year), str(month_num))
        bands_merged = merge_monthly_sat_bands(bucket, sat_monthly_dir_path)
        for band_name, band_merged in bands_merged.items():
            create_sat_eopatch(bounds, band_merged, save=True,
                               file_name=f"eopatch_{year}_{month_num}_{img_loc.replace("/", "")}_{band_name}",
                               dir_path= os.path.join(SAT_IMG_FOLDER, DPT_FOLDER), bucket=bucket)
        del bands_merged
#def get_sat_images(bucket, ):

def merge_monthly_sat_bands(bucket, month_dir):
    '''Merge all shots of a month for each band
    Shots are filtered by maskcloud (scl: scene classification) and merged
    Parameters:
    month_dir: path to the directory of given month
    Return:
    dict of bands, key are band names and values are merge data'''
    shots_list=list(bucket.list_dir(month_dir))
    shots_list = list(set([os.path.dirname(blob.name) for blob in shots_list]))
    num_shots = len(shots_list)
    bands_merged = {band: np.zeros((1))for band in BANDS_USED}
    for i in range(num_shots):
        print(f"processing shot {i}")
        # Open the file using rasterio
        with rasterio.Env(GCS=True):
            cld_file_path  = os.path.join(bucket.bucket_name, shots_list[i], 'SCL.tif')
            with rasterio.open('gs://'+cld_file_path) as cld_src:
            # tranform from shape (1, 5490, 5490) to shape (1, 10980, 10980)
                cld = np.repeat(np.repeat(np.isin(cld_src.read(), [4, 5, 6, 7]), 2, axis=2), 2, axis=1)
            for key, band_merged in bands_merged.items():
                print(f"processing {shots_list[i]} {key}.tif ...")
                band_file_path  = os.path.join(bucket.bucket_name, shots_list[i], key+'.tif')
                with rasterio.open('gs://'+band_file_path) as band_src:
                    band_data = band_src.read()
                if key == "B11": # from shape (1, 5490, 5490) to shape (1, 10980, 10980)
                    band_data = np.repeat(np.repeat(band_data, 2, axis=2), 2, axis=1)
                if band_merged.shape != band_data.shape:
                    band_merged = np.zeros(band_data.shape, dtype=np.uint8)
                band_merged[band_merged==0]= (band_data*(np.repeat(cld, band_data.shape[0], axis=0)))[band_merged==0]
                bands_merged[key] = band_merged
                print(f"bands merged {bands_merged.keys()}")
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
