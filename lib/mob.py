from lib2to3 import pygram
from re import sub
from matplotlib.pyplot import grid, sca
import py
import pygame
from sympy import im

from lib.coords import Coords, RefSys
from lib.display import Display
from lib.dotdict import dotdict
from lib.movable import Movable
from .settings import SCREEN_DPI, IMAGES

def scalemob(img, metrics, front, oversize):
    tmargin = 114
    bmargin = 3
    lmargin = 3
    h0 = int(metrics.h/2-tmargin-bmargin)
    w0 = metrics.w-2*lmargin
    aspect = h0/w0
    subimg = pygame.Surface((w0, h0), pygame.SRCALPHA, 32)
    if not front:
        img = pygame.transform.flip(img, flip_x = False, flip_y = True)
    subimg.blit(img, (0, 0), pygame.Rect(lmargin, metrics.h/2+bmargin, w0, h0) )
    subimg = pygame.transform.smoothscale(subimg, size=(int(oversize * SCREEN_DPI) , int(oversize * SCREEN_DPI * aspect)))
    return aspect, subimg #pygame.transform.flip(subimg, False, True)

class Mob(Movable):
    def __init__(self, mobname):
        Movable.__init__(self)
        self.mobname = mobname
        info = dotdict(Mob.MOBS[mobname])
        self.info = info
        fpath = f"{IMAGES}/mobs/{info.img}"
        img = pygame.image.load(fpath)
        oversize = info.get('oversize', 1)
        self.oversize = oversize
        metrics = img.get_rect()
        #self.front = pygame.transform.scale(pygame.transform.chop(img, pygame.Rect(0, metrics.h/2, metrics.w, metrics.h/2-30)), (SCREEN_DPI, SCREEN_DPI * metrics.h / metrics.w))
        #self.back = pygame.transform.chop(img, pygame.Rect(0, metrics.h/2-30, metrics.w, 30))
        #self.front = pygame.transform.smoothscale(img, (100,300))
        
        aspect, self.front = scalemob(img, metrics, 1, oversize)
        aspect, self.back = scalemob(img, metrics, 0, oversize)
        scale_metrics = self.front.get_rect()
        self.handle = Coords(scale_metrics.w/2, scale_metrics.h, RefSys.WORLD)
        print("handle",self.handle)
        #self.handle = Coords(0, scale_metrics.h + 12, RefSys.WORLD)
        self.dir = 0

    def __repr__(self):
        return f"Mob<{self.mobname}>({self.pos},{self.dir},{self.oversize},{self.handle})"

    def render(self, display : Display):
        if not self.dir:
            img = self.front
        else:
            img = self.back
        display.blit(img, self.pos - self.handle)
        display.circle(self.pos)

    def contains_point(self, coord : Coords):
        cx, cy = coord.p
        mx, my = (self.pos - self.handle).p
        rect = self.front.get_rect()
        
        if cx > mx and cx < mx + rect.w and cy > my and cy < my + rect.h:
            return True
        return False

    @classmethod 
    def load(cls, mob):
        return Mob(mob)


    MOBS = {
        "zombie-dwarf-1": {
            "img": "Zombie - Dwarf - 01.png"
        },
        "vhalak": {
            "img": "Vhalak.png",
            "oversize": 1.25
        }
    }