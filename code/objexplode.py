#explosion class

import random
import pygame
from pygame.locals import *
import game, gfx


images = []


def load_game_resources():
    global images

    img = gfx.load('explosion.png')
    images.extend(gfx.animstrip(img))



class Explode:
    def __init__(self, pos, move=(0,0)):
        self.time = 0.0
        self.move = [float(move[0])*.9, float(move[1])*.9]
        self.pos = [float(pos[0])+self.move[0], float(pos[1])+self.move[1]]
        self.life = float(len(images))
        self.rect = images[0].get_rect()
        self.rect.center = pos
        self.dead = 0
        self.lastrect = None

    def erase(self, background):
        if self.lastrect:
            r = background(self.lastrect)
            if self.dead:
                gfx.dirty(r)

    def draw(self, gfx):
        img = images[int(self.time)]
        r = gfx.surface.blit(img, self.rect)
        gfx.dirty2(r, self.lastrect)
        self.lastrect = r

    def tick(self, speedadjust):
        self.time += speedadjust * .7
        self.pos[0] += speedadjust * self.move[0]
        self.pos[1] += speedadjust * self.move[1]
        self.rect.center = self.pos
        if self.time >= self.life:
            self.dead = 1


