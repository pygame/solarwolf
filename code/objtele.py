#teleport in to start animation class

import random
import pygame
from pygame.locals import *
import game, gfx


images = []


def load_game_resources():
    global images
    for i in range(1,11):
        img = gfx.load('tele_in-%02d.gif'%i)
        images.append(img)

   

class Tele:
    def __init__(self, pos):
        self.images = images
        self.numclocks = len(images)
        self.clocks = 0
        self.rect = images[0].get_rect()
        self.rect.center = pos
        self.dead = 0

    def erase(self, background):
        r = background(self.rect)
        if self.dead:
            gfx.dirty(r)

    def draw(self, gfx):
        img = images[self.clocks]
        r = gfx.surface.blit(img, self.rect)
        gfx.dirty(r)

    def tick(self, speedadjust):
        self.clocks += 1
        if self.clocks == self.numclocks:
            self.dead = 1
