#explosion class

import random, math
import pygame
from pygame.locals import *
import game, gfx


images = []


def load_game_resources():
    global images
    images = gfx.animstrip(gfx.load('smoke.png'))
    if gfx.surface.get_bytesize()>1: #16 or 32bit
        i = 1
        for img in images:
            img.set_alpha((1.8-math.log(i))*40, RLEACCEL)
            i += 1



class Smoke:
    def __init__(self, pos):
        self.clocks = 0
        self.rect = images[0].get_rect()
        self.rect.center = pos
        offset = random.randint(-7,7), random.randint(-7,7)
        self.rect = self.rect.move(offset)
        self.lastrect = self.rect
        self.dead = 0
        self.drift = random.randint(-1, 1), random.randint(-1, 1)
        self.speed = random.randint(2, 4)
        self.current = 0
        self.life = random.randint(12, 20)

    def erase(self, background):
        r = background(self.rect)
        if self.dead:
            gfx.dirty(r.inflate(1, 2))

    def draw(self, gfx):
        frame = int(min(self.clocks // 5, 3))
        img = images[frame]
        r = gfx.surface.blit(img, self.rect)
        gfx.dirty(r.inflate(1, 2))

    def tick(self, speedadjust):
        self.current += 1
        if self.current >= self.speed:
            self.current = 0
            self.rect = self.rect.move(self.drift)

        self.clocks += 1
        if self.clocks >= self.life:
            self.dead = 1


