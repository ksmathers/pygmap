from lib.coords import Coords, RefSys
from lib.lerp import Lerp
from lib.movable import Movable
from lib.moveplan import MovePlan
from .settings import DISPLAY_HEIGHT, DISPLAY_WIDTH
import pygame

class Display(Movable):
    def __init__(self):
        Movable.__init__(self)
        self.size = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.center_coord = Coords(DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2)
        self.surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.mplan = MovePlan(self, 52)

    def blit(self, img : pygame.Surface, imgpos : Coords):
        self.surf.blit(img, (imgpos - self.pos).p)

    def move_by(self, by_pos : Coords):
        self.pos = self.pos + by_pos

    def clear(self):
        self.surf.fill(pygame.color.Color(0,0,0))

    def circle(self, center : Coords, radius = 5, color = pygame.Color(180,30,180)):
        pygame.draw.circle(self.surf, center=(center-self.pos).p, radius= radius, color= color)

    def flip(self):
        pygame.display.flip()
        self.clear()
    
    def mpos_to_world(self, pos):
        mx, my = pos
        return self.pos + Coords(mx, my, RefSys.WORLD)

    def recenter(self, ctr_pos : Coords):
        self.mplan.add_waypoint(ctr_pos - self.center_coord)

    @property
    def center(self):
        return self.pos + self.center_coord

    def update(self):
        if self.mplan:
            self.mplan.update()