from typing import Callable
from lib.coords import Coords
from lib.lerp import Lerp
from lib.movable import Movable
from lib.settings import SCREEN_DPI
from lib.timer import Timer

class MovePlan:
    def __init__(self, movable : Movable, speed_ips:float, plan_ended:Callable = None):
        self.movable = movable
        self.speed = speed_ips
        self.waypoints = []
        self.lerp = None
        self.timer = None
        self.lmag = 0
        self.plan_ended = plan_ended

    def add_waypoint(self, p : Coords):
        self.waypoints.append(p)

    def update(self):
        if self.lerp is None:
            if len(self.waypoints) >= 1:
                p = self.waypoints.pop(0)
                self.lerp = Lerp(self.movable.pos, p)
                self.lmag = self.lerp.mag
                self.duration = self.lmag / (self.speed * SCREEN_DPI)
                self.timer = Timer(self.duration)
            else:
                if self.plan_ended:
                    self.plan_ended(self)
        if self.lerp:
            ratio = self.timer.ratio()
            p = self.lerp.at(ratio)
            #print(ratio,p)
            self.movable.move_to(p)
            if ratio >= 1:
                self.lerp = None
                self.timer = None
        
