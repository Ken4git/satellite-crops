from google.cloud.storage import Client, transfer_manager
from satellitecrops.params import *
import pathlib
from eolearn.core import (
    EOPatch,
    OverwritePermission
    )

class BucketConnector:
    def __init__(self, bucket_name="satellite_crops") -> None:
        self.client = Client()
        self.bucket_name = bucket_name
        self.bucket = self.client.bucket(self.bucket_name)

    def upload_sat_patch(self, eopatch, file_name, dir_path=f"eolearn_data/{ZONE_TYPE}/{DPT}"):
        eopatch.save("~/tmp/eopatch", overwrite_permission=OverwritePermission.OVERWRITE_FEATURES)
        eopatch_folder = pathlib.Path("~/tmp/eopatch")
        eopatch_file_paths = [item for item in eopatch_folder.iterdir() if item.is_file()]
        blob_path = f"{dir_path}/{file_name}"
        blob = self.bucket.blob(blob_path)
        relative_paths = [path.relative_to(eopatch_folder) for path in eopatch_file_paths]
        string_paths = [str(path) for path in relative_paths]
        results = transfer_manager.upload_many_from_filenames(self, string_paths, source_directory=eopatch_folder)
        return results

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
