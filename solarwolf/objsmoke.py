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

#explosion class

import random, math
import pygame
import gfx


images = []


def load_game_resources():
    global images
    images = gfx.animstrip(gfx.load('smoke.png'))
    if gfx.surface.get_bytesize()>1: #16 or 32bit
        i = 1
        for img in images:
            img.set_alpha((1.8-math.log(i))*40, pygame.RLEACCEL)
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


