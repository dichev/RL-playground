import numpy as np

def mean_cum(count, mean, amount):
    sum = mean * count
    return (sum + amount) / (count + 1)

def softmax(values, tau = 1):
    exp = np.exp(np.array(values) / tau)
    return exp / np.sum(exp)


def split_number(size, n):
    chunks = [size // n] * n
    diff = size - sum(chunks)
    if diff:
        chunks[-1] += diff
    return chunks