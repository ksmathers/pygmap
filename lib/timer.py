
from time import time

class Timer:
    def __init__(self, cycle_sec : float = 1.0):
        self.tstart = time()
        self.cycle_sec = cycle_sec

    def elapsed(self):
        return time()-self.tstart

    def ratio(self):
        if self.cycle_sec == 0:
            return 1.0
        return self.elapsed()/self.cycle_sec