import os
import gzip
import numpy as np

def create_Xy(path:str):
    '''
    Create X and y from eopatches.
    '''
    X_path = []
    Y_path = []

    for root, dirs, files in os.walk(path):
        for name in files:
            if name == 'BANDS.npy.gz':
                X_path.append(os.path.join(root, name))
            if name == 'MASK.npy.gz':
                Y_path.append(os.path.join(root, name))

    X = []
    y = []

    # Unzip
    for i,x_path in enumerate(X_path):
        with gzip.open(x_path) as f:
            X.append(np.load(f))

    for i,y_path in enumerate(Y_path):
        with gzip.open(y_path) as f:
            y.append(np.load(f))

    y = np.stack(y)
    X = np.stack(X)

    return X , y