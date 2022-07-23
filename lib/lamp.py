import pygame
from sklearn.neighbors import DistanceMetric
from lib.display import Display
from lib.settings import SCREEN_DPI, DISPLAY_HEIGHT, DISPLAY_WIDTH


class Lamp:
    def __init__(self, distance):
        self.distance = distance
        self.radius = SCREEN_DPI * distance
        self.surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)

    def update(self, mobs, display : Display):
        surf = self.surface
        surf.fill(pygame.Color(0,0,0,255))

        for m in mobs:
            mpos = (m.pos - display.pos).p
            pygame.draw.circle(surf, pygame.Color(100,0,0,128), mpos, self.radius)
        for m in mobs:
            mpos = (m.pos - display.pos).p
            pygame.draw.circle(surf, pygame.Color(100,0,0,0), mpos, self.radius/2)

        display.blit(surf, display.pos)