#box class

import random
import pygame
from pygame.locals import *
import game, gfx


images = []


def load_game_resources():
    global images
    for i in range(1,3):
        img = gfx.load('popbox%d.gif'%i)
        images.append(img)

   

class PopBox:
    def __init__(self, pos):
        self.clocks = 4
        self.img = images[0]
        self.rect = self.img.get_rect()
        self.rect.center = pos
        self.dead = 0

    def erase(self, background):
        background(self.rect)
        if self.dead:
            gfx.dirty(self.rect)

    def draw(self, gfx):
        r = gfx.surface.blit(self.img, self.rect)
        gfx.dirty(r)

    def tick(self, speedadjust):
        self.clocks -= 1
        if self.clocks == 2:
            self.img = images[1]
        elif not self.clocks:
            self.dead = 1
