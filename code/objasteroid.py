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

#powerup class

import random
import pygame
import game, gfx

images = []
origsize = 0,0

def load_game_resources():
    global images, origsize
    anim = gfx.animstrip(gfx.load('asteroid.png'))
    origsize = anim[0].get_size()
    for x in range(36):
        set = []
        for img in anim:
            r = pygame.transform.rotate(img, x*10+8)
            set.append(r.convert())
        images.append(set)


class Asteroid:
    def __init__(self):
        self.speed = game.asteroidspeed
        self.colliderect = pygame.Rect((0, 0), origsize).inflate(-8, -8)
        self.reposition()
        self.dead = 0
        self.time = 0
        self.rotspeed = 0.2

    def reposition(self):
        self.images = random.choice(images)
        self.image = self.images[0]#[0]

        self.movex = random.random() * 2.0 - 1.0
        diff = 1.0 - abs(self.movex)
        self.movey = random.choice((diff, -diff))
        r = random.randint(0, 1200)
        if r < 700:
            self.pos = [float(r), 0.0]
        else:
            self.pos = [0.0, float(r - 700)]

        self.animspeed = (random.random() + 2.0) * .1
        if random.random() < .5:
            self.animspeed = -self.animspeed

        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.rect.move_ip(-20, -20)
        self.colliderect.center = self.rect.center


    def predictrect(self):
        posx = (self.pos[0] + 24.0 * self.speed * self.movex) % 740
        posy = (self.pos[1] + 24.0 * self.speed * self.movey) % 640
        rect = pygame.Rect(self.colliderect)
        rect.center = posx, posy
        rect.move_ip(-20, -20)
        return rect

    def erase(self, background):
        r = background(self.rect)
        gfx.dirty(r)

    def draw(self, gfx):
        r = gfx.surface.blit(self.image, self.rect)
        gfx.dirty(r)

    def tick(self, speedadjust):
        self.time += speedadjust
        anm = int(self.time * self.animspeed)
        anim = self.images
        self.image = anim[anm % len(anim)]

        posx = (self.pos[0] + speedadjust*self.speed * self.movex) % 740
        posy = (self.pos[1] + speedadjust*self.speed * self.movey) % 640
        if abs(posx - self.pos[0])>300 or abs(posy-self.pos[1])>300:
            self.reposition()
        self.pos[0] = posx
        self.pos[1] = posy
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.rect.move_ip(-20, -20)
        self.colliderect.center = self.rect.center

