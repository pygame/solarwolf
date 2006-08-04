#simple enemy class

import pygame, pygame.image
from pygame.locals import *
import gfx, game, random

images = []

def load_game_resources():
    #load shot graphics
    global images
    img = gfx.load('bullet.gif')
    images.append(img)
    images.append(pygame.transform.flip(img, 0,1))
    images.append(pygame.transform.flip(img, 1,1))
    images.append(pygame.transform.flip(img, 1,0))


class Shot:
    def __init__(self, pos, move):
        self.move = move
        self.images = images
        self.numframes = len(images)
        self.frame = random.random() * 3.0
        self.rect = self.images[0].get_rect()
        self.rect.center = pos
        self.lastrect = None
        self.dead = 0
        self.pos = list(self.rect.topleft)

    def prep(self, screen):
        pass

    def erase(self, background):
        if self.lastrect:
            background(self.lastrect)
            if self.dead:
                gfx.dirty(self.lastrect)
                self.lastrect = None

    def draw(self, gfx):
        frame = int(self.frame) % self.numframes
        img = self.images[frame]
        r = gfx.surface.blit(img, self.rect)
        gfx.dirty2(r, self.lastrect)
        self.lastrect = r

    def tick(self, speedadjust = 1.0):
        self.frame += speedadjust * .5
        self.pos[0] += self.move[0] * speedadjust
        self.pos[1] += self.move[1] * speedadjust
        self.rect.topleft = self.pos
        if not gfx.rect.colliderect(self.rect):
            self.dead = 1
        return self.dead

