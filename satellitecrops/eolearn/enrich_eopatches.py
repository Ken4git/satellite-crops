### ML
import numpy as np

import os

### EO-Learn / SentinelHub ###
from sentinelhub import BBox
from eolearn.core import (
    EOPatch,
    OverwritePermission
    )
# geom manipulation
import rasterio
import geopandas as gpd
from shapely.geometry import box

def add_data2subpatch(sat_patch, eopatch):
    '''Creates a new eopatch, which is eopatch enriched with sat_patch data

    Parameters:
    sat_patch (eopatch): an eopatch which contains the data to add
    eopatch (eopatch): the "subpatch" (small eopatch) you want to add data to

    Returns:
    eopatch: a new eopatch, which is eopatch enriched with sat_patch data

    Example:
    for instance eopatch contains mask_timeless and sat_patch contains
    data or data_timeless, this data will be added to the eopatch,
    a new eopatch is returned
    '''
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
    '''Update eopatches files with sat_patch data

    Parameters:
    sat_patch (eopatch): an eopatch which contains the data to add
    eopatches_files (list): list of pathes to eopatches in EOPATCH_FOLDER,
    the eopatches being the small eopatches you want to add data to

    Returns:
    nothing returned

    See add_data2subpatch(sat_patch, eopatch) function to see how the data is
    added to each subpatch
    '''
    for eo_file in eopatches_files:
        eo_file_path = os.path.join(EOPATCH_FOLDER, eo_file)
        eopatch = EOPatch.load(eo_file_path, lazy_loading=True)
        new_eopatch = add_data2subpatch(sat_patch, eopatch)
        new_eopatch.save(eo_file_path, overwrite_permission=OverwritePermission.OVERWRITE_FEATURES)
        del new_eopatch
        del eopatch

def add_data_from_sat_patches_to_eopatches(eopatches_files, sat_patches_files):
    '''Update eopatches files with sat_patch data from multiple files

    Parameters:
    sat_patch_files (list): list of pathes to eopatches which contains the data to add
    eopatches_files (list): list of pathes to eopatches in EOPATCH_FOLDER,
    the eopatches being the small eopatches you want to add data to

    Returns:
    nothing returned

    See add_data2subpatch(sat_patch, eopatch) function to see how the data is
    added to each subpatch
    '''
    for file_path in sat_patches_files:
        sat_patch = EOPatch.load(file_path, lazy_loading=True)
        for eo_file in eopatches_files:
            bbox_file_path = os.path.join(eo_file, "bbox.geojson")
            gdf =  gpd.read_file(bbox_file_path)
            if sat_patch.bbox.geometry.contains(gdf['geometry'][0]):
                eopatch = EOPatch.load(eo_file, lazy_loading=True)
                new_eopatch = add_data2subpatch(sat_patch, eopatch)
                new_eopatch.save(eo_file, overwrite_permission=OverwritePermission.OVERWRITE_FEATURES)
            del new_eopatch
            del eopatch
        del sat_patch
