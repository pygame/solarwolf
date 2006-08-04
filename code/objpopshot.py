#box class

import random
import pygame
from pygame.locals import *
import game, gfx


images = []
explode_frames = 11

def load_game_resources():
    global images
    images = gfx.animstrip(gfx.load('popshot.png'), 18)



class PopShot:
    def __init__(self, pos):
        self.clocks = 0
        self.life = explode_frames
        self.rect = images[0].get_rect()
        self.rect.center = pos
        self.dead = 0

    def erase(self, background):
        r = background(self.rect)
        if self.dead:
            gfx.dirty(r)

    def draw(self, gfx):
        img = images[self.clocks/3]
        r = gfx.surface.blit(img, self.rect)
        gfx.dirty(r)

    def tick(self, speedadjust):
        self.clocks += 1
        if self.clocks == self.life:
            self.dead = 1
