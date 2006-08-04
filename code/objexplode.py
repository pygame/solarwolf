#explosion class

import random
import pygame
from pygame.locals import *
import game, gfx


images = []


def load_game_resources():
    global images
    for i in range(1,7):
        img = gfx.load('explosion%d.gif'%i)
        images.append(img)

   

class Explode:
    def __init__(self, pos):
        self.click = 0
        self.life = 22
        self.rect = images[0].get_rect()
        self.rect.center = pos
        self.dead = 0

    def erase(self, background):
        r = background(self.rect)
        if self.dead:
            gfx.dirty(r)

    def draw(self, gfx):
        img = images[self.click / 4]
        r = gfx.surface.blit(img, self.rect)
        gfx.dirty(r)

    def tick(self, speedadjust):
        self.click += 1
        if self.click == self.life:
            self.dead = 1


