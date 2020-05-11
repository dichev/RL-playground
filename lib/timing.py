from time import time
from contextlib import contextmanager
from dataclasses import astuple, dataclass

@contextmanager
def timer(msg = 'Elapsed time'):
    startAt = time()
    yield
    print(f'{msg}: {time() - startAt} ms')




@dataclass
class Measurement:
    duration: int
    frames:   int
    speed:    float
    def __iter__(self):
        return iter(astuple(self))

class Measure:

    def __init__(self):
        self.time = time()
        self.frames = 0

    def tick(self):
        self.frames +=1

    def get_duration(self):
        return time() - self.time

    def finish(self) -> Measurement:
        duration = time() - self.time
        frames = self.frames
        speed = frames / max(1, duration) # todo: use nanosecs
        self.reset()
        return Measurement(duration, frames, speed)

    def reset(self):
        self.time = time()
        self.frames = 0