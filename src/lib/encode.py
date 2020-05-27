import numpy as np

def one_hot(vectors, value):
    if isinstance(vectors, np.ndarray):
        vectors = vectors.tolist()

    index = vectors.index(value)
    encoded = np.zeros(len(vectors))
    encoded[index] = 1
    return encoded


def scale_minmax(vectors, min=None, max=None):
    min = min or vectors.min()
    max = max or vectors.max()
    vectors = (vectors - min) / (max - min)
    return vectors
