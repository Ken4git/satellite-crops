import os
import gzip
import numpy as np
from satellitecrops.params import *

def select_min_crops_coverage(X, y, coverage):
    max_background = int(PXL_WIDTH) * int(PXL_HEIGHT)
    X_parsed = []
    y_parsed = []

    for idx, _y in enumerate(y):
        recap_tile = np.unique(_y, return_counts=True)
        recap = dict(zip(recap_tile[0], recap_tile[1]))
        tile_coverage = (max_background - recap[0]) / max_background
        if tile_coverage >= coverage:
            X_parsed.append(X[idx])
            y_parsed.append(_y)
    return np.stack(X_parsed), np.stack(y_parsed)

def create_Xy(path:str, min_crops_coverage:float=0):
    '''
    Create X and y from eopatches.
    '''

    print(f'Creating X and y with minimum coverage of {min_crops_coverage}...')
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
            f.close()

    for i,y_path in enumerate(Y_path):
        with gzip.open(y_path) as f:
            y.append(np.load(f))
            f.close()


    y = np.stack(y)
    X = np.stack(X)

    X, y = select_min_crops_coverage(np.stack(X), np.stack(y), min_crops_coverage)

    print(f'X created with shape {X.shape}')
    print(f'y created with shape {y.shape}')

    return X, y
