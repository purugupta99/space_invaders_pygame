#!/usr/bin/python

from characters import *


class Missile(Character):
    def __init__(self, x, y, myfont, color, symbol, velocity):
        super().__init__(x, y, myfont, color, symbol)
        self.velocity = velocity

    def moveUp(self):
        self.y_pos += self.velocity

    def hit(self, x, y, limit):
        if self.y_pos <= y and x <= self.x_pos <= x+limit:
            return True


class Bullet(Missile):
    def __init__(self, x, y, myfont, color, velocity):
        super().__init__(x, y, myfont, color, 'i', velocity)
        self.type = 'bullet'


class Taser(Missile):
    def __init__(self, x, y, myfont, color, velocity):
        super().__init__(x, y, myfont, color, '|', velocity)
        self.type = 'taser'
