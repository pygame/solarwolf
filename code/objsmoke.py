#explosion class

import random, math
import pygame
from pygame.locals import *
import game, gfx


images = []


def load_game_resources():
    global images
    for i in range(1,5):
        img = gfx.load('smoke%d.gif'%i)
        img.set_colorkey((255, 49, 255), RLEACCEL)
        if gfx.surface.get_bytesize()>1:
            img.set_alpha((1.8-math.log(i))*40, RLEACCEL)
        images.append(img)



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
        frame = min(self.clocks / 5, 3)
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


