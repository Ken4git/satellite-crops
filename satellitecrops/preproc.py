import numpy as np

def scaling(arr:list, pos:int, a:float=0, b:float=1, clip:bool=True):
    '''
    Performs a linear transformation on each channel of a given satellite image. Array must be of dimension 4.

    normalized_band = (value - c) * (b - a) / (d - c) + a

    arr : array to be scaled with a linear transformation
    pos : index of the number of channels
    a : lower limit of the resulting range
    b : upper limit of the resulting range
    clip : whether to bound the interval or not
    '''

    if pos != arr.ndim-1:
        if pos != -1:
            arr = np.moveaxis(arr, pos, -1)

    # Linear normalization https://medium.com/sentinel-hub/how-to-normalize-satellite-images-for-deep-learning-d5b668c885af
    res = []

    for i in range(arr.shape[-1]):
        band = arr[:,:,:,i]
        c = np.percentile(band, 1)
        d = np.percentile(band, 99)
        normalized_band = (band - c) * (b - a) / (d-c) + a
        res.append(normalized_band)

    if clip==True:
        return np.clip(np.stack(res, axis=pos),0,1)

    return np.stack(res, axis=pos)
