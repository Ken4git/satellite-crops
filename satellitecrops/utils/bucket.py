from google.cloud.storage import Client
from satellitecrops.params import *


class BucketConnector:
    def __init__(self, bucket_name="satellite_crops") -> None:
        self.client = Client()
        self.bucket_name = bucket_name
        self.bucket = self.client.bucket(self.bucket_name)

    def list_dir(self, dir_path):
        prefix=dir_path+"/"
        return self.client.list_blobs(self.bucket_name, prefix=prefix)

    def get_blob(self, file_name, dir_path=f"eolearn_data/{ZONE_TYPE}/{DPT}"):
        blob_path = f"{dir_path}/{file_name}"
        blob = self.bucket.blob(blob_path)
        with blob.open("r") as fd:
            content = fd.read()
            return content

    def get_jp2_image(self, file_name,  dir_path=f"eolearn_data/{ZONE_TYPE}/{DPT}"):
        blob_path = f"{dir_path}/{file_name}"
        blob = self.bucket.blob(blob_path)
        with blob.open("rb") as fd:
            content = fd.read()
            return content
