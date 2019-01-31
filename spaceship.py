#!/usr/bin/python
from characters import *


class Spaceship(Character):

    def __init__(self, x, y, myfont, color):
        super().__init__(x, y, myfont, color, '<^_^>')

    def moveRight(self):
        self.x_pos += 80

    def moveLeft(self):
        self.x_pos -= 80

    def noChange(self):
        self.x_pos += 0
