import numpy as np

def scaling(arr:list, pos:int, a:float=0, b:float=1):
    '''
    Performs a linear transformation on each channel of a given satellite image.

    normalized_band = (value - c) * (b - a) / (d-c) + a

    arr : array to be scaled with a linear transformation
    pos : index of the number of channels
    a : lower limit of the resulting range
    b : upper limit of the resulting range
    '''

    if pos != arr.ndim-1:
        if pos != -1:
            arr = np.moveaxis(arr, pos, -1)

    # Convert DN to Reflectance
    reflectance = arr / 10000.0

    # Linear normalization https://medium.com/sentinel-hub/how-to-normalize-satellite-images-for-deep-learning-d5b668c885af
    res = []

    c = np.percentile(reflectance, 1)
    d = np.percentile(reflectance, 99)

    for i in range(reflectance.shape[-1]):
        slices = (slice(None),) * (reflectance.ndim - 1) + (1,)
        band = reflectance[slices]
        normalized_band = (band - c) * (b - a) / (d-c) + a
        res.append(normalized_band)

    return np.stack(res, axis=pos)
