
import math
from typing import Tuple

from pygame import Surface
import pygame

from lib.display import Display
from lib.settings import DISPLAY_HEIGHT, DISPLAY_WIDTH, MAPSCALE

def cmp(x,y):
    return -1 if x < y else 1

def fint(x):
    if x > 0:
        return int(x+1e-4)
    else:
        return int(x-1e-4)

def clamp(nv, nmin, nmax):
    if nv < nmin: nv = nmin
    if nv > nmax: nv = nmax
    return nv

def enlighten(p):
    p = 1 - ((1-p)*3/8)
    return p

def range_shader(x,y):
    return 20-math.log(x*x+y*y+1)

def fraction(n,m):
    if n == 0:
        return (1,0)
    while n % 2 == 0:
        n //= 2
        m //= 2
        if n == 1: break
    return (n,m)

def vecs(m=64):
    tmp  = [ fraction(i,m) for i in range(m+1) ]
    for xs,ys in [(1,1), (-1, -1)]:
        for x,y in tmp:
            yield (xs * x, ys * y)
            if x != y and x != 0 and y != 0:
                yield (ys * y, xs * x)
        for x,y in tmp:
            yield (-ys * y, xs * x)
            if x != y and x != 0 and y != 0:
                yield (xs * x, -ys * y)

class Lighting:
    MAXINT = int(1e31)
    WALL = 0xff00ff

    def __init__(self, size : Tuple[int,int], display : Display):
        self.display = display
        self.size = size
        self.overlay = Surface(size, pygame.SRCALPHA)
        self.load_wall()

    def load_wall(self):
        _img = pygame.image.load("./images/maps/walls.png")
        scalex, scaley = MAPSCALE
        rect = _img.get_rect()
        self.walls = walls = pygame.transform.scale(_img, (int(rect.w * scalex), int(rect.h * scaley)))


    def follow(self, vec, d):
        dsqr = d * d
        x,y = vec
        xa = abs(x)
        ya = abs(y)
        xs = cmp(x,0)
        ys = cmp(y,0)
        xi = 0
        yi = 0
        if xa > ya:
            r = ya / xa
            while xi*xi + yi*yi < dsqr:
                yield (xs * xi, ys * fint(yi))
                xi += 1
                yi += r
        else:
            r = xa / ya
            while xi*xi + yi*yi < dsqr:
                yield (xs * fint(xi), ys * yi)
                yi += 1
                xi += r        
                
    def spill_light(self, vec): 
        fld = self.overlay
        d = self.size
        x0, y0 = (self.size//2, self.size//2)
        for x,y in self.follow(vec, d):
            #print(x0, x, y0, y)
            if fld[x0+x][y0+y] == Lighting.WALL:
                break
            else:
                #fld[x0+x][y0+y] = enlighten(fld[x0+x][y0+y]+0.1)
                fld[x0+x][y0+y] = range_shader(x,y)

    def update(self):
        w,h = self.size
        wx = (DISPLAY_WIDTH//2 - w//2)
        hy = (DISPLAY_HEIGHT//2 - h//2)
        self.overlay.blit(self.display.surf, (0, 0), (wx, hy, w, h))
        px = pygame.PixelArray(self.overlay)
        px[h//2:h//2+3,:] = 0
        px = None
        self.display.blit(self.overlay, (wx, hy))


    def illuminate(self):
        SIZE=128
        fld = self.overlay
        pt = (DISPLAY_WIDTH//2, DISPLAY_HEIGHT//2)
            
        for v in vecs(64): 
            self.spill_light(pt, v)