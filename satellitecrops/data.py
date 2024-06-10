import os
import gzip
import numpy as np

def create_Xy(path:str):
    '''
    Create X and y from eopatches.
    '''

    print('Creating X and y ...')
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
            print(i)
            X.append(np.load(f))
            f.close()

    for i,y_path in enumerate(Y_path):
        with gzip.open(y_path) as f:
            y.append(np.load(f))
            f.close()

    y = np.stack(y)
    X = np.stack(X)

    print('X and y created ... ')

    return X , y
