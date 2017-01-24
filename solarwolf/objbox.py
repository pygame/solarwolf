#box class

import random
import pygame
from pygame.locals import *
import game, gfx, snd


boximages = []
yboximages = []
rboximages = []
wboximages = []
popimages = []
spikeimages = []
wspikeimages = []

def load_game_resources():
    global boximages, yboximages, rboximages, wboximages
    global popimages, spikeimages, wspikeimages
    imgs = gfx.load_raw('boxes.png')
    origpal = imgs.get_palette()
    boximages = gfx.animstrip(imgs)

    pal = [(g,g,b) for (r,g,b) in origpal]
    imgs.set_palette(pal)
    yboximages = gfx.animstrip(imgs)

    pal = [(g,b,b) for (r,g,b) in origpal]
    imgs.set_palette(pal)
    rboximages = gfx.animstrip(imgs)

    pal = [min(g+60,255) for (r,g,b) in origpal]
    imgs.set_palette(list(zip(pal,pal,pal)))
    wboximages = gfx.animstrip(imgs)

    popimages = gfx.animstrip(gfx.load('popbox.png'))


    spikes = gfx.load_raw('spikeball.png')
    origpal = spikes.get_palette()
    spikeimages = gfx.animstrip(spikes)
    pal = [(min(r+100,255),min(g+100,255),min(b+100,255)) for r,g,b in origpal]
    spikes.set_palette(pal)
    wspikeimages = gfx.animstrip(spikes)

    snd.preload('boxhit', 'yboxhit')


class Box:
    def __init__(self, pos, touches):
        self.rotate = random.random() * 90.0
        self.rotspeed = random.random() * 2.0 + 2.0
        if random.randint(0, 1):
            self.rotspeed = -self.rotspeed
        self.rect = boximages[0].get_rect().move(pos)
        self.touches = touches
        self.touching = 0
        self.firsttouch = 2.0
        self.dead = 0
        self.popped = 0
        self.imglists = wboximages, boximages, yboximages, rboximages
        self.numframes = len(self.imglists[0])

    def erase(self, background):
        r = background(self.rect)
        if self.dead:
            gfx.dirty(r)

    def draw(self, gfx):
        frame = int(self.rotate)%self.numframes
        if self.popped:
            img = popimages[int(self.popped)]
        elif self.firsttouch > 0.0:
            img = self.imglists[0][frame]
        else:
            img = self.imglists[int(self.touches)][frame]
        r = gfx.surface.blit(img, self.rect)
        gfx.dirty(r)

    def tick(self, speedadjust):
        self.rotate += self.rotspeed * speedadjust * .2
        if self.firsttouch > 0.0:
            self.firsttouch -= speedadjust
        elif self.popped:
            if self.popped >= 1.9:
                self.dead = 1
            else:
                self.popped = min(self.popped + speedadjust * .35, 1.9)
        elif not self.touches:
            self.popped = .01

    def playercollide(self, rect):
        if self.touching:
            self.touching = self.rect.colliderect(rect)
            return 0
        elif self.touches and self.rect.colliderect(rect):
            self.touches -= 1
            if self.touches:
                self.firsttouch = 4.0
                self.touching = 1
                snd.play('yboxhit', 1.0, self.rect.centerx)
                return 2
            self.firsttouch = 2.0
            snd.play('boxhit', 1.0, self.rect.centerx)
            return 1
        return 0

    def pop(self):
        self.touches = 0
        self.firsttouch = 2.0


class Spike:
    blockrocks = 0
    def __init__(self, pos):
        self.rotate = random.random() * 90.0
        self.rotspeed = random.random() * 1.0 + 1.0
        if random.randint(0, 1):
            self.rotspeed = -self.rotspeed
        self.images = spikeimages, wspikeimages
        self.numframes = len(self.images[0])
        self.rect = self.images[0][0].get_rect().move(pos)
        self.dead = 0
        self.popped = 0
        self.armed = 0
        self.armtime = 0.0

    def erase(self, background):
        r = background(self.rect)
        if self.dead:
            gfx.dirty(r)

    def draw(self, gfx):
        frame = int(self.rotate)%self.numframes
        img = self.images[not self.armed][frame]
        r = gfx.surface.blit(img, self.rect)
        gfx.dirty(r)

    def tick(self, speedadjust):
        self.rotate += self.rotspeed * speedadjust * .2
        self.armtime += speedadjust
        self.armed = self.armtime > 14.0

