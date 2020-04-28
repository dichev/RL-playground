import numpy as np

def mean_cum(count, mean, amount):
    sum = mean * count
    return (sum + amount) / (count + 1)

def softmax(values, tau = 1):
    exp = np.exp(np.array(values) / tau)
    return exp / np.sum(exp)

