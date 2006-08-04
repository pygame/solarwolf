#simple enemy class

import pygame, pygame.image
from pygame.locals import *
import gfx, game, random, math

images = []
allimages = []

#glowstuff adjusted from updateglow func
glowtime = 0.0
glowset = 0

def load_game_resources():
    #load shot graphics
    global images, allimages
    img = gfx.load_raw('fire.png')
    origpal = img.get_palette()
    img.set_colorkey(img.get_at((0,0)))
    images = gfx.animstrip(img)
    allimages.append(images)

    for x in range(10, 181, 10):
        pal = [(max(r-x*.2,0), max(g-x*.4,0), min(b+x*.3,255))
                for (r,g,b) in origpal]
        img.set_palette(pal)
        allimages.append(gfx.animstrip(img))


def updateglow(speedadjust):
    global glowtime, glowset, allimages
    glowtime += speedadjust * .2
    glowset = int((math.sin(glowtime)*.5+.5) * len(allimages))


class Shot:
    blockrocks = 1
    def __init__(self, pos, move):
        self.move = move
        self.images = images
        self.numframes = len(self.images)
        self.frame = random.random() * 3.0
        self.rect = self.images[0].get_rect()
        self.rect.center = pos
        self.lastrect = None
        self.dead = 0
        self.pos = list(self.rect.topleft)
        self.time = 0.0
        self.numbrights = float(len(images))

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
        img = allimages[glowset][frame]
        r = gfx.surface.blit(img, self.rect)
        gfx.dirty2(r, self.lastrect)
        self.lastrect = r

    def tick(self, speedadjust = 1.0):
        self.frame += speedadjust * .5
        self.pos[0] += self.move[0] * speedadjust
        self.pos[1] += self.move[1] * speedadjust
        self.time += speedadjust * .1
        self.images = images[int(math.cos(self.time)*self.numbrights)]
        self.rect.topleft = self.pos
        if not gfx.rect.colliderect(self.rect):
            self.dead = 1
        return self.dead

