# solarwolf - collecting and dodging arcade game
# Copyright (C) 2006  Pete Shinners <pete@shinners.org>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#box class

import random
import pygame
from pygame.locals import *
import game, gfx, snd

rbox_color = (255, 60, 60)
gbox_color = (60, 255, 60)
bbox_color = (60, 60, 255)

rbigboximages = []
gbigboximages = []
bbigboximages = []

rboximages = []
gboximages = []
bboximages = []
wboximages = []

popimages = []

spikeimages = []
wspikeimages = []

def red_animation(palette, images):
    images.set_palette([(g,b,b) for (r,g,b) in palette])
    return gfx.animstrip(images)

def blue_animation(palette, images):
    images.set_palette([(b,b,g) for (r,g,b) in palette])
    return gfx.animstrip(images)

def white_animation(palette, images):
    intensities = [min(g+60,255) for (r,g,b) in palette]
    images.set_palette([(i,i,i) for i in intensities])
    return gfx.animstrip(images)

def load_game_resources():
    global rbigboximages, gbigboximages, bbigboximages, wbigboximages
    global rboximages, gboximages, bboximages, wboximages
    global popimages, spikeimages, wspikeimages

    ### Big Boxes ###

    imgs = gfx.load_raw('bigboxes.png')
    origpal = imgs.get_palette()
    gbigboximages = gfx.animstrip(imgs)

    rbigboximages = red_animation(origpal, imgs)
    bbigboximages = blue_animation(origpal, imgs)

    ### Small Boxes ###

    imgs = gfx.load_raw('boxes.png')
    origpal = imgs.get_palette()
    gboximages = gfx.animstrip(imgs)

    rboximages = red_animation(origpal, imgs)
    bboximages = blue_animation(origpal, imgs)
    wboximages = white_animation(origpal, imgs)

    ### Popping box ###

    popimages = gfx.animstrip(gfx.load('popbox.png'))

    ### Spike ###

    spikes = gfx.load_raw('spikeball.png')
    origpal = spikes.get_palette()
    spikeimages = gfx.animstrip(spikes)

    pal = [(min(r+100,255),min(g+100,255),min(b+100,255)) for r,g,b in origpal]
    spikes.set_palette(pal)
    wspikeimages = gfx.animstrip(spikes)

    ### Sounds ###

    snd.preload('boxhit', 'yboxhit')


class Box:
    def __init__(self, pos, touches):
        self.rotate = random.random() * 90.0
        self.rotspeed = random.random() * 2.0 + 2.0
        if random.randint(0, 1):
            self.rotspeed = -self.rotspeed
        self.rect = rboximages[0].get_rect().move(pos)
        self.touches = touches
        self.touching = 0
        self.firsttouch = 2.0
        self.dead = 0
        self.popped = 0
        self.imglists = wboximages, rboximages, gboximages, bboximages
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
            img = self.imglists[self.touches][frame]
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

