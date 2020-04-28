import numpy as np

def moving_avg(x, N=50): # TODO: check me
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)