
from enum import Enum
import math

from .settings import SCREEN_DPI

class RefSys(Enum):
    WORLD=1
    GAMEGRID=2


class Coords:
    def __init__(self, x : float, y : float, refsys:RefSys = RefSys.WORLD):
        """Defines a 2D coordinate pair
        
        Args:
            x :float: Cartesian horizontal
            y :float: Cartesian vertical
            refsys :RefSys: 
                WORLD - pixel coordinates, origin at top, left
                GAMEGRID - one inch square grid, origin at top, left
        """
        self.ref = refsys
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Coords({self.x},{self.y},{self.ref})"

    def translate(self, refsys:RefSys):
        xoff = 0
        yoff = 0
        if self.ref == refsys:
            return self
        if self.ref == RefSys.WORLD and refsys == RefSys.GAMEGRID:
            return Coords((self.x / SCREEN_DPI) - xoff, (self.y / SCREEN_DPI) - yoff, RefSys.GAMEGRID)
        if self.ref == RefSys.GAMEGRID and refsys == RefSys.WORLD:
            return Coords((self.x + xoff) * SCREEN_DPI, (self.y + yoff) * SCREEN_DPI, RefSys.WORLD)
    
    def __add__(self, other):
        tmp = other.translate(self.ref)
        return Coords(self.x + tmp.x, self.y + tmp.y, self.ref)

    def __sub__(self, other):
        tmp = other.translate(self.ref)
        return Coords(self.x - tmp.x, self.y - tmp.y, self.ref)

    def __div__(self, fval:float):
        x, y = self.p
        return Coords(x / fval, y / fval, RefSys.WORLD)

    def __mul__(self, fval:float):
        x, y = self.p
        return Coords(x * fval, y * fval, RefSys.WORLD)

    @property
    def p(self):
        """point in world coordinates"""
        tmp = self.translate(RefSys.WORLD)
        return (tmp.x, tmp.y)

    @property
    def r(self):
        """point as rho, theta"""
        tmp = self.translate(RefSys.WORLD)
        return (tmp.mag, tmp.angle)

    @property
    def mag(self):
        """magnitude from origin in world coordinates"""
        x,y = self.p
        return math.sqrt(x*x+y*y)

    @property
    def angle(self):
        """angle from origin in world coordinates"""
        x,y = self.p
        return math.atan2(y,x)

    @property
    def v(self):
        tmp = self.translate(RefSys.GAMEGRID)
        return (tmp.x, tmp.y)



        
