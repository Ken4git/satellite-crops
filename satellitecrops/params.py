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
