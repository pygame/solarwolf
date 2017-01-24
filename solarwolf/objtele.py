#teleport in to start animation class

import random
import pygame
from pygame.locals import *
import game, gfx


images = []

def load_game_resources():
    global images, imagesbaddie

    img = gfx.load('ship-teleport.png')
    images.extend(gfx.animstrip(img))



class Tele:
    def __init__(self, pos):
        self.images = images
        self.numclocks = len(images)
        self.clocks = 0.0
        self.rect = images[0].get_rect()
        self.rect.topleft = pos
        self.dead = 0
        self.rocksclear = 0

    def erase(self, background):
        r = background(self.rect)
        if self.dead:
            gfx.dirty(r)

    def draw(self, gfx):
        frame = min(int(self.clocks), len(self.images)-1)
        img = self.images[frame]
        r = gfx.surface.blit(img, self.rect)
        gfx.dirty(r)

    def tick(self, speedadjust):
        if self.clocks < 3.0 or self.rocksclear:
            self.clocks += speedadjust * .6
            if self.clocks >= self.numclocks:
                self.dead = 1
