import os
import numpy as np
import geopandas as gpd
import pandas as pd
import gzip
from satellitecrops.params import *


def create_npy_file():
    eo_loc = []
    bands = []
    masks = []
    eopatches_path = os.path.join(DATA_PATH, "eopatches")
    files = os.listdir(eopatches_path)

    for i in range(len(files) - 1):

        eo_path = os.path.join(eopatches_path, f"eopatch_{i}", "bbox.geojson")
        eo_loc.append(gpd.read_file(eo_path))

        mask_path = os.path.join(eopatches_path, f"eopatch_{i}", "mask_timeless", "MASK.npy.gz")
        mask = gzip.GzipFile(mask_path, "r")
        masks.append(np.load(mask))

        band_path = os.path.join(eopatches_path, f"eopatch_{i}", "data_timeless", "BANDS.npy.gz")
        band = gzip.GzipFile(band_path, "r")
        bands.append(np.load(band))

    bands_df = np.stack(bands, axis=0)
    masks_df = np.stack(masks, axis=0)
    eo_loc_df = pd.concat(eo_loc, ignore_index=True, axis=0)

    eo_loc_df.to_file("./data/dataframe.gpkg", driver="GPKG", layer="name")
    np.save("./data/my_images", bands_df)
    np.save("./data/my_labels", masks_df)


if __name__ == "__main__":
    create_npy_file()
