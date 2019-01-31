#!/usr/bin/python


class Character(object):
    def __init__(self, x, y, myfont, color, symbol):
        self.x_pos = x
        self.y_pos = y
        self.myfont = myfont
        self.color = color
        self.symbol = myfont.render(symbol, False, color)

    def getWidth(self):
        return self.symbol.get_width()

    def getHeight(self):
        return self.symbol.get_height()

    def draw(self, screen):
        screen.blit(self.symbol, (self.x_pos, self.y_pos))
