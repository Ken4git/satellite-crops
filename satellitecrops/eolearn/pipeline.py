### Data manipulation ###
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

### Utils ###
import os
import sys
### eolearn tools
from satellitecrops.eolearn.eolearn_workflow import make_and_run_workflow
from satellitecrops.eolearn.create_eopatches import get_zone_to_patch, create_bbox_of_zone, get_parcelles_from_db, zone2sat_patch
from satellitecrops.eolearn.enrich_eopatches import add_sat_patch_to_eopatch, add_data_from_sat_patches_to_eopatches
from satellitecrops.utils.sql_connector import SQLConnection
from satellitecrops.params import *
from satellitecrops.utils.bucket import BucketConnector

from colorama import Fore, Style

# from tqdm import tqdm

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

def create_patches_from_parcelles():
    init_env()
    bucket = BucketConnector()
    dpt_zone = get_zone_to_patch(bucket).to_crs(LOCAL_CRS)
    bbox_list, info_list = create_bbox_of_zone(dpt_zone)
    parcelles_path = get_parcelles_from_db(dpt_zone)
    make_and_run_workflow(parcelles_path, bbox_list)

def main():
    init_env()
    bucket = BucketConnector()
    create_patches_from_parcelles()
    sat_patch = zone2sat_patch(bucket)
    add_sat_patch_to_eopatch(os.listdir(EOPATCH_FOLDER), sat_patch)

from satellitecrops.eolearn.create_eopatches import create_sat_eopatches
def create_patches():
    init_env()
    bucket = BucketConnector()
    bucket.upload_sat_patch("test", "test_dir")
    #print(create_sat_eopatches(bucket, "30/T/XP", 2019))

def main_local():
    init_env()
    print(Fore.MAGENTA + "\n⏳ Loading satellite image of the zone" + Style.RESET_ALL)
    sat_dir_path = os.path.join(DATA_PATH, "sat_images")
    add_data_from_sat_patches_to_eopatches(os.listdir(EOPATCH_FOLDER), sat_dir_path)

if __name__ == "__main__":
    create_patches()
