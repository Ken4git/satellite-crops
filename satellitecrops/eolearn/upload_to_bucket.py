from satellitecrops.utils.bucket import BucketConnector
from satellitecrops.params import *
import os

def upload_patches_to_bucket():
    bucket = BucketConnector(bucket_name=BUCKET_NAME).bucket
    eopatches_path = os.path.join(DATA_PATH, "eopatches")
    files = os.listdir(eopatches_path)

    for i in range(len(files) - 1):
        mask_path = os.path.join(eopatches_path, f"eopatch_{i}", "mask_timeless", "MASK.npy.gz")
        blob_path = f"eolearn_data/dpt/landes/MASK_{i}.npy.gz"
        blob = bucket.blob(blob_path)
        blob.upload_from_filename(mask_path)
        print(f"Succeffuly uploaded {mask_path}")

        band_path = os.path.join(eopatches_path, f"eopatch_{i}", "data_timeless", "BANDS.npy.gz")
        blob_path = f"eolearn_data/dpt/landes/BANDS_{i}.npy.gz"
        blob = bucket.blob(blob_path)
        blob.upload_from_filename(band_path)
        print(f"Succeffuly uploaded {band_path}")

if __name__ == "__main__":
    upload_patches_to_bucket()
