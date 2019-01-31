#!/usr/bin/python
from characters import *


class Alien(Character):
    def __init__(self, x, y, myfont, color, time):
        super().__init__(x, y, myfont, color, '(-)_(-)')
        self.spawn_time = time
        self.tag = False

    def tagged(self):
        self.symbol = self.myfont.render("()_()", False, self.color)
        self.tag = True
