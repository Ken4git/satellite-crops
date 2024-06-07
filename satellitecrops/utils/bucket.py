from google.cloud.storage import Client
from satellitecrops.params import *


class BucketConnector:
    def __init__(self, bucket_name="satellite_crops") -> None:
        self.client = Client()
        self.bucket_name = bucket_name
        self.bucket = self.client.bucket(self.bucket_name)


    def get_blob(self, file_name):
        blob_path = f"eolearn_data/{ZONE_TYPE}/{DPT}/{file_name}"
        blob = self.bucket.blob(blob_path)
        with blob.open("r") as fd:
            content = fd.read()
            return content
