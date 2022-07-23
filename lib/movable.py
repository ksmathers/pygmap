from lib.coords import Coords

class Movable:
    def __init__(self):
        self.pos = Coords(0,0)

    def move_to(self, pos):
        self.pos = pos