import numpy as np
from collections import Counter

def mean_cum(count, mean, amount):
    sum = mean * count
    return (sum + amount) / (count + 1)


def sum_collection(lst:list) -> dict:
    counter = Counter()
    for obj in lst:
        counter.update(obj)
    return dict(counter)

def mean_collection(lst:list) -> dict:
    n = len(lst)
    sums = sum_collection(lst)
    means = { key: val/n for key, val in sums.items()}
    return means


def softmax(values, tau = 1):
    exp = np.exp(np.array(values) / tau)
    return exp / np.sum(exp)


def split_number(size, n):
    chunks = [size // n] * n
    diff = size - sum(chunks)
    if diff:
        chunks[-1] += diff
    return chunks