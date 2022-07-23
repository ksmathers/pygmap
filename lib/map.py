from typing import List
from lib.dotdict import dotdict
from lib.coords import Coords, RefSys
from lib.display import Display
from .settings import DISPLAY_HEIGHT, DISPLAY_WIDTH, IMAGES, MAPSCALE, SCREEN_DPI
from .util import clamp
import pygame

class Map:
    def __init__(self, mapname):
        self.mapname = mapname
        attrs = dotdict(Map.MAPS[mapname])
        self.attrs = attrs
        _img = pygame.image.load(f"{IMAGES}/maps/{attrs.img}")
        self.rect = _img.get_rect()
        scale = MAPSCALE
        self.w = self.rect.w * scale[0] / SCREEN_DPI
        self.h = self.rect.h * scale[1] / SCREEN_DPI
        self.img = pygame.transform.scale(_img, (self.w * SCREEN_DPI, self.h * SCREEN_DPI))
        
        self.img = pygame.transform.scale(_img, (self.rect.w * scale[0], self.rect.h * scale[1]))
        #self.img = pygame.transform.scale(_img, (attrs.w * SCREEN_DPI, attrs.h * SCREEN_DPI))
        #scale = (attrs.w * SCREEN_DPI / self.rect.w, attrs.h * SCREEN_DPI / self.rect.h) 
        self.pos = self._coord('pos', scale=scale)
        self.spawn = self._coord('spawn', RefSys.GAMEGRID)
        self.scale = scale
        print(self)

    def __repr__(self):
        return f"Map<{self.mapname}>({self.w},{self.h},{self.pos},{self.scale})"

    def _coord(self, attr, ref : RefSys = RefSys.WORLD, scale = (1.0, 1.0)):
        sx, sy = scale
        if attr in self.attrs:
            x,y = self.attrs[attr]
            return Coords(x * sx, y * sy, ref)
        return None

    def __getattr__(self, attrib):
        return self.attrs[attrib]

    def grid(self, x, y):
        xoff = 0.5
        yoff = .75
        return Coords(x+xoff, y+yoff, RefSys.GAMEGRID)+self.pos

    def contains_point(self, coord : Coords):
        cx, cy = coord.p
        mx, my = self.pos.p
        rect = self.img.get_rect()

        
        if cx > mx - Map.HBORDER and cx < mx + rect.w + Map.HBORDER and cy > my - Map.VBORDER and cy < my + rect.h + Map.VBORDER:
            return True
        return False

    def render(self, display : Display):
        display.blit(self.img, self.pos)

    def spawn_coord(self):
        spos = self.attrs.get('spawn', None)
        if not spos is None:
            x, y = spos
            spos = self.grid(x, y)
        return spos

    HBORDER = 3 * SCREEN_DPI
    VBORDER = 3 * SCREEN_DPI
    MAPS = {
            "area1": {
                'img': "Area 1-min.jpg",
                'pos': (147, 9513),
                'w': 22,
                'h': 17,
                'spawn': (8, 16)
            },
            "area2a": {
                'img': "Area 2a-min.jpg",
                'pos': (2248, 6662),
                'w': 17,
                'h': 19,
                'c01': ( 14, 19),
                'c02': ( 15, 19)
            },
            "area2b": {
                'img': "Area 2b-min.jpg",
                'pos': (7, 5462),
                'w': 15,
                'h': 28,
                'c21': ( 15, 10),
                'c22': ( 15, 11)
            },
            "area3a": {
                'img': "Area 3a-min.jpg",
                'pos': (3015, 9211)
            },
            "area3b": {
                'img': "Area 3b-min.jpg",
                'pos': (5100, 11461)
            },
            "area4": {
                'img': "Area 4-min.jpg",
                'pos': (3530, 11243)
            },
            "area5": {
                'img': "Area 5-min.jpg",
                'pos': (5988, 11242)
            },
            "area6": {
                'img': "Area 6-min.jpg",
                'pos': (4784, 7356)
            },
            "area7": {
                'img': "Area 7-min.jpg",
                'pos': (5813, 7411)
            },
            "area8": {
                'img': "Area 8-min.jpg",
                'pos': (6898, 8459)
            },
            "area9a": {
                'img': "Area 9a-min.jpg",
                'pos': (2345, 4713)
            },
            "area9b": {
                'img': "Area 9b-min.jpg",
                'pos': (5248, 5462)
            },
            "area10": {
                'img': "Area 10-min.jpg",
                'pos': (7, 2311)
            },
            "area11": {
                'img': "Area 11-min.jpg",
                'pos': (2999, 3164)
            },
            "area12": {
                'img': "Area 12-min.jpg",
                'pos': (4502, 2161)
            },
            "area13a_14": {
                'img': "Area 13a_14-min.jpg",
                'pos': (7720, 6060)
            },
            "area13b_15": {
                'img': "Area 13b_15-min.jpg",
                'pos': (7348, 4110)
            },
            "area16": {
                'img': "Area 16-min.jpg",
                'pos': (6900, 700)
            },
            "area17": {
                'img': "Area 17-min.jpg",
                'pos': (5250, 296)
            },
            "area18": {
                'img': "Area 18-min.jpg",
                'pos': (2701, -30)
            },
            "area19_20": {
                'img': "Area 19_20-min.jpg",
                'pos': (98, 14)
            },
            "walls": {
                'img': "walls.png",
                'pos': (0,0)
            }
        }

    @classmethod
    def load(cls, mapname):
        return Map(mapname)