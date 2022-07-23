from lib.coords import Coords, RefSys
from time import time
import math

class Lerp:
    def __init__(self, start:Coords, end:Coords):
        self.start = start
        self.end = end
        self.delta = (end-start)

    def at(self, ratio : float):
        if ratio <= 0.0:
            return self.start
        if ratio >= 1.0:
            return self.end
        return self.start + (self.delta * ratio)

    @property
    def mag(self):
        return self.delta.mag

class Slerp:
    def __init__(self, start:Coords, end:Coords):
        self.start = start.r
        self.end = end.r
        self.delta_rho = self.end[0] - self.start[0]
        self.delta_theta = self.end[1] - self.start[1]

    def at(self, ratio : float):
        if ratio <= 0.0:
            polar = self.start
        elif ratio >= 1.0:
            polar = self.end
        else:
            rho = self.start[0] + self.delta_rho * ratio
            theta = self.start[1] + self.delta_theta * ratio
            polar = (rho, theta)

        rho, theta = polar
        x = rho * math.cos(theta)
        y = rho * math.sin(theta)
        return Coords(x, y, RefSys.WORLD)


