import numpy as np

def scaling(arr:list,
            pos:int,
            a:float=0,
            b:float=1,
            clip:bool=True,
            temporal:bool=False):
    '''
    Performs a linear transformation on each channel of a given satellite image.
    https://medium.com/sentinel-hub/how-to-normalize-satellite-images-for-deep-learning-d5b668c885af

    normalized_band = (value - c) * (b - a) / (d - c) + a

    arr: Data to be scaled.
    pos: Index of the number of channels.
    a: Lower limit of the resulting range.
    b: Upper limit of the resulting range.
    clip: Whether to bound the values to [0,1].
    temporal: If True, arr integrates temporal dimension (ie arr.ndim == 5)
    '''

    # Ensuring number of channels corresponds to the last index
    if pos != arr.ndim-1:
        if pos != -1:
            arr = np.moveaxis(arr, pos, -1)

    # Linear normalization
    res = []

    for i in range(arr.shape[-1]):
        band = arr[:,:,:,:,i] if temporal else arr[:,:,:,i]
        c = np.percentile(band, 1)
        d = np.percentile(band, 99)
        normalized_band = (band - c) * (b - a) / (d-c) + a
        res.append(normalized_band)

    # Clipping between [0,1]
    if clip==True:
        return np.clip(np.stack(res, axis=pos),0,1)

    return np.stack(res, axis=pos)

def clean_y(y:np.ndarray):
    d = {}

    for i in range(len(np.unique(y))):
        if i != np.unique(y)[i]:
            d[y[i]] = i

    for k,v in d.items():
        y[y==k] = v

    return y
