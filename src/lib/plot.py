import numpy as np
import os, re, time

def moving_avg(x, N=50): # TODO: check me
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)


def tboard_next_id(path='runs/', pattern=r'#(\d+)'):
    last = 0
    for dir_name in os.listdir(path):
        found = re.findall(pattern, dir_name)
        if found:
            last = max(last, int(found[0]))

    next_id = '#' + str(last + 1)
    return next_id

