import pandas as pd
import numpy as np

from google.cloud import storage
import gzip
import io

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from satellitecrops.registry import load_model
from satellitecrops.preproc import scaling
from satellitecrops.params import *

app = FastAPI()
app.state.model = load_model()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/predict")
def predict(eopatch_id:int):
    """
    Make a single prediction.
    """

    # Retrieve eopatch directly from the bucket
    client = storage.Client()
    url = 'https://storage.cloud.google.com/satellite_crops/eolearn_data/dpt/landes/my_images.npy'

    blobs = client.bucket('satellite_crops').blob(f'eolearn_data/dpt/landes/BANDS_{eopatch_id}.npy.gz')

    blob_data = blobs.download_as_bytes()

    with gzip.GzipFile(fileobj=io.BytesIO(blob_data)) as f:
        X = np.load(f)

    model = app.state.model
    X = np.expand_dims(X, axis=0)
    X_pred_processed = scaling(X,1)
    X_pred_processed = np.moveaxis(X_pred_processed, 1, 3)

    return {'img': model.predict(X_pred_processed)[0].tolist()} # Get first element because shape is (1, img_height, img_size, channels)

@app.get("/")
def root():
    return {
    'greeting': 'Hello'
}
