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

import random
import pygame
from pygame.locals import *
import game, gfx, objpopshot


images = []
debris = []


def load_game_resources():
    global images, debris

    img = gfx.load('explosion.png')
    images.extend(gfx.animstrip(img))

    debrisnames = 'base', 'bubble', 'motor'
    debristemp = []
    for d in debrisnames:
        strip = gfx.load('debris-' + d + '.png')
        #strip.insert(0, strip[0])
        debristemp.append(gfx.animstrip(strip))
    #need to to rotations?
    for i in (0,1,1,2,2):
        debris.append(debristemp[i])
    for d in range(1,5):
        strip = gfx.load('debris%d.png'%d)
        debris.append(gfx.animstrip(strip))



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
        self.time += speedadjust * .5
        self.pos[0] += speedadjust * self.move[0]
        self.pos[1] += speedadjust * self.move[1]
        self.rect.center = self.pos
        if self.time >= self.life:
            self.dead = 1




class Debris:
    def __init__(self, part, pos, move=(0,0)):
        self.images = debris[part]
        self.time = 0.0
        self.move = [float(move[0])*1.6, float(move[1])*1.6]
        self.move[0] += (random.random()-.5) * 2.0
        self.move[1] += (random.random()-.5) * 2.0
        self.pos = [float(pos[0])+self.move[0]*1.5, float(pos[1])+self.move[1]*1.5]
        self.life = float(len(self.images))
        self.rect = self.images[0].get_rect()
        self.rect.center = pos
        self.dead = 0
        self.lastrect = None
        self.speed = random.random() * .15 + 0.15

    def erase(self, background):
        if self.lastrect:
            r = background(self.lastrect)
            if self.dead:
                gfx.dirty(r)

    def draw(self, gfx):
        img = self.images[int(self.time)]
        r = gfx.surface.blit(img, self.rect)
        gfx.dirty2(r, self.lastrect)
        self.lastrect = r

    def tick(self, speedadjust):
        self.time += speedadjust * self.speed
        self.pos[0] += speedadjust * self.move[0]
        self.pos[1] += speedadjust * self.move[1]
        self.rect.center = self.pos
        if self.time >= self.life:
            self.dead = 1


def superexplode(pos, move):
    sprites = []
    sprites.append(Explode(pos, move))
    for d in range(len(debris)):
        sprites.append(Debris(d, pos, move))
    for x in range(4):
        newpos = list(pos)
        newpos[0] += (random.random()-.5) * 30
        newpos[1] += (random.random()-.5) * 30
        pop = objpopshot.PopShot(newpos)
        sprites.append(pop)

    return sprites

