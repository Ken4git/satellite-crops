import os
import pandas as pd

### GCP ###

GCP_PROJECT_NAME = os.environ.get("GCP_PROJECT_NAME")
GCP_REGION = os.environ.get("GCP_REGION")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
# Compute Engine
INSTANCE=os.environ.get("INSTANCE")

MODEL_TARGET = os.environ.get("MODEL_TARGET")
### Local pathes ###
LOCAL_REGISTRY_PATH = os.path.join(os.path.expanduser('~'), ".lewagon", "satellite-crops", "training_outputs")
DATA_DIR_LOCAL=os.environ.get("DATA_DIR_LOCAL")

### POSTGRES SQL ###
DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
DB_INSTANCE = os.environ.get("DB_INSTANCE")

# Satellite Data
SAT_IMG_FOLDER =os.environ.get("SAT_IMG_FOLDER")
DPT_FOLDER=os.environ.get("DPT_FOLDER")
IMG_SOURCE = os.environ.get("IMG_SOURCE")
IMG_ORIGIN =os.environ.get("IMG_ORIGIN")
IMG_LOC=os.environ.get("IMG_LOC")
YEAR=os.environ.get("YEAR")

# Bands used
BANDS_USED=['B02','B08', 'B11', 'TCI']


### EO LEARN ###
EOPATCH_FOLDER=os.environ.get("EOPATCH_FOLDER")
DPT=os.environ.get("DPT")
ZONE_TYPE=os.environ.get("ZONE_TYPE")
LOCAL_CRS=os.environ.get("LOCAL_CRS")


MAPPING = pd.read_csv("./mapping_crops.csv")

### EO LEARN ###

DPT = os.environ.get("DPT")
ZONE_TYPE = os.environ.get("ZONE_TYPE")
LOCAL_CRS = os.environ.get("LOCAL_CRS")
DATA_PATH = os.path.join(os.path.dirname(os.getcwd()), "satellite-crops", "data", "departments", DPT)
EOPATCH_FOLDER = os.path.join(DATA_PATH, "eopatches")
EOPATCH_SAMPLES_FOLDER = os.path.join(DATA_PATH, "eopatches_sampled")
RESULTS_FOLDER = os.path.join(DATA_PATH, "results")
PXL_WIDTH = os.environ.get("PXL_WIDTH")
PXL_HEIGHT = os.environ.get("PXL_HEIGHT")
