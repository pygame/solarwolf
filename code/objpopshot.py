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
