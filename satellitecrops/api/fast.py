import pandas as pd
import numpy as np


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from satellitecrops.registry import load_model
from satellitecrops.preproc import scaling

X = np.load('./data/kaggle_dataset/X.npy')


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
def predict():
    """
    Make a single prediction.
    """
    img=X[0]
    print(img.shape)
    model = app.state.model
    img = np.expand_dims(img, axis=0)
    X_pred_processed = scaling(img,1)
    X_pred_processed = np.moveaxis(X_pred_processed, 1, 3)
    print(X_pred_processed.shape)
    return {'img': model.predict(X_pred_processed)[0].tolist()} # Get first element because shape is (1, img_height, img_size, channels)

@app.get("/")
def root():
    return {
    'greeting': 'Hello'
}
