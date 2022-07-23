from lib2to3 import pygram
from re import L
from typing import List
import matplotlib as mpl
import pygame
from pygame.locals import *
from lib import display
from lib.coords import Coords, RefSys
from lib.lamp import Lamp
from lib.lighting import Lighting
from lib.moveplan import MovePlan
from lib.settings import SCREEN_DPI, DISPLAY_HEIGHT, DISPLAY_WIDTH
from lib.map import Map
from lib.mob import Mob
from lib.display import Display



 
class MyGame:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = DISPLAY_WIDTH, DISPLAY_HEIGHT
        self.clock = None
        self.mobs : List[Mob] = []
        self.moveplans : List[MovePlan] = []
        self.maps : List[Map] = []
        self.selected_obj = None

    def end_of_movement(self, mplan):
        self.moveplans.remove(mplan)
        self.m1_circuit()

    def m1_circuit(self):
        ips = 2.5
        map = self.maps[1]
        mplan = MovePlan(self.mobs[0], ips, self.end_of_movement)
        mplan.add_waypoint(map.grid(13,12))
        mplan.add_waypoint(map.grid(2,12))
        mplan.add_waypoint(map.grid(2,8))
        mplan.add_waypoint(map.grid(13,8))
        self.moveplans.append(mplan)
 
    @property 
    def map(self):
        return self.maps[0]

    def on_init(self):
        ips = 2.5
        pygame.init()
        self.display = Display()
        for map in Map.MAPS:
            self.maps.append(Map.load(map))
        #print(self.map)
        m1 = Mob.load("zombie-dwarf-1")
        m1.move_to( self.maps[1].grid(13,8))
        print(m1)
        m2 = Mob.load("vhalak")
        m2.move_to (self.map.spawn_coord())
        self.mobs.append(m1)
        self.mobs.append(m2)
        self.lamp = Lamp(6)

        self.m1_circuit()
        self.display.move_to(m2.pos - Coords(DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2))
        self.lighting = Lighting(200,200, self.display)
        self._running = True

    def select_object(self, pos):
        mcoord = self.display.mpos_to_world(pos)
        for m in self.mobs:
            if m.contains_point(mcoord):
                #print(f"click on {m}")
                self.selected_obj = m
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.select_object(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            if self.selected_obj:
                self.selected_obj.move_to(self.display.mpos_to_world(event.pos))
        elif event.type == pygame.MOUSEBUTTONUP:
            self.selected_obj = None
            self.display.recenter(self.mobs[1].pos)
        else:
            print(event)

    def on_loop(self, dt):
        ips = 2
        for mp in self.moveplans:
            mp.update()
        if not self.selected_obj:
            self.display.update()


    def on_render(self, dt):
        for m in self.maps:
            if m.contains_point(self.display.center):
                m.render(self.display)
        for m in self.mobs:
            m.render(self.display)
        #self.lamp.update(self.mobs, self.display)
        self.lighting.update()
        self.display.flip()

    def on_cleanup(self):
        pygame.quit()
 
    def run(self):
        if self.on_init() == False:
            self._running = False
 
        clock = pygame.time.Clock()
        while( self._running ):
            dt = clock.tick(60)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop(dt)
            self.on_render(dt)
        self.on_cleanup()
 
if __name__ == "__main__" :
    app = MyGame()
    app.run()