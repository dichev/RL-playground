from time import time
from contextlib import contextmanager

@contextmanager
def timer():
    startAt = time()
    yield
    print(f'Elapsed time: {time() - startAt} ms')