#jumptowarp animation class

import random
import pygame
from pygame.locals import *
import game, gfx


images = []
CLOCK_MULTIPLIER = 3


def load_game_resources():
    global images
    for i in range(1,16):
        img = gfx.load('warp_%04d.gif'%i)
        images.append(img)
    # Hold the blank frame for a few extra counts.
    images[12:] = [images[11]]*2 + [images[-1], images[-2], images[-2], images[-1]]
    # Add on an extra bit of twinkle at the end.
    #images.extend([images[-2],images[-2]])
   

class Warp:
    def __init__(self, pos):
        self.images = images
        self.numclocks = len(images)*CLOCK_MULTIPLIER
        self.clocks = 0
        self.rect = images[0].get_rect()
        self.rect.center = pos
        self.dead = 0

    def erase(self, background):
        r = background(self.rect)
        if self.dead:
            gfx.dirty(r)

    def draw(self, gfx):
        img = images[self.clocks/CLOCK_MULTIPLIER]
        r = gfx.surface.blit(img, self.rect)
        gfx.dirty(r)

    def tick(self, speedadjust):
        self.clocks += 1
        # Ship moves to the right until it disappears, then the
        # "twinkle" is stationary.
        if self.clocks/CLOCK_MULTIPLIER < 12:
            self.rect.left += 2
            self.rect.top -= 1
        if self.clocks == self.numclocks:
            self.dead = 1
