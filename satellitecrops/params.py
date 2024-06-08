import os

### GCP ###

GCP_PROJECT_NAME = os.environ.get("GCP_PROJECT_NAME")
GCP_REGION = os.environ.get("GCP_REGION")


### POSTGRES SQL ###

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
DB_INSTANCE = os.environ.get("DB_INSTANCE")


### EO LEARN ###

DPT = os.environ.get("DPT")
ZONE_TYPE = os.environ.get("ZONE_TYPE")
LOCAL_CRS = os.environ.get("LOCAL_CRS")
DATA_PATH = os.path.join(os.path.dirname(os.getcwd()), "satellite-crops", "data", "departments", DPT)
EOPATCH_FOLDER = os.path.join(DATA_PATH, "eopatches")
EOPATCH_SAMPLES_FOLDER = os.path.join(DATA_PATH, "eopatches_sampled")
RESULTS_FOLDER = os.path.join(DATA_PATH, "results")
