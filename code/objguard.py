#simple enemy class

import os
import pygame, pygame.image
from pygame.locals import *
import game, gfx

images = []
teleimages = []
openframes = 8.0
shootframes = 5.0
totalframes = 15.0

def load_game_resources():
    #load ship graphics
    global images
    i = gfx.load('baddie.png')
    i = pygame.transform.flip(i, 0, 1)
    i.set_colorkey((0,0,0))
    imgs = gfx.animstrip(i, 64)
    del imgs[9] #clean animation a little
    images.append(imgs)

    for x in (90, 180, 270):
        rotimgs = []
        for i in imgs:
            r = pygame.transform.rotate(i, x)
            rotimgs.append(r)
        images.append(rotimgs)

    i = gfx.load('baddie-teleport.png')
    i = pygame.transform.flip(i, 0, 1)
    i.set_colorkey((0,0,0))
    imgs = gfx.animstrip(i, 64)
    teleimages.append(imgs)
    for x in (90, 180, 270):
        rotimgs = []
        for i in imgs:
            r = pygame.transform.rotate(i, x)
            rotimgs.append(r)
        teleimages.append(rotimgs)


class Guard:
    def __init__(self, type):
        self.images = images[type]
        img = self.images[0]
        self.type = type
        self.dead = 0
        self.rect = img.get_rect()
        if type == 0: #top
            self.rect.bottomleft = game.arena.topleft
            self.move = [game.guard_speed, 0]
        elif type == 1: #left
            self.rect.bottomright = game.arena.bottomleft
            self.move = [0, -game.guard_speed]
        elif type == 2: #bottom
            self.rect.topright = game.arena.bottomright
            self.move = [-game.guard_speed, 0]
        else: #right
            self.rect.topleft = game.arena.topright
            self.move = [0, game.guard_speed]
        self.lastrect = None
        self.firenow = 0
        self.bullets = 0
        self.openstate = 0
        self.time = 0.0
        self.frame = 0
        self.pos = list(self.rect.topleft)

        self.killed = 1


    def shotinfo(self):
        if not self.firenow:
            return None, None
        self.firenow = 0
        self.bullets -= 1

        speed = game.shot_speed
        if self.type == 0: #top
            return self.rect.center, (0, speed)
        elif self.type == 1: #left
            return self.rect.center, (speed, 0)
        elif self.type == 2: #bottom
            return self.rect.center, (0, -speed)
        else: #right
            return self.rect.center, (-speed, 0)


    def erase(self, background):
        if self.lastrect:
            r = background(self.lastrect)
            if self.dead:
                gfx.dirty(r)

    def draw(self, gfx):
        if not self.killed:
            img = self.images[self.frame]
            r = gfx.surface.blit(img, self.rect)
            gfx.dirty2(r, self.lastrect)
            self.lastrect = r


    def tick(self, speedadjust = 1.0):
        if self.killed:
            return

        #move
        self.pos[0] += self.move[0] * speedadjust
        self.pos[1] += self.move[1] * speedadjust
        self.rect.topleft = self.pos
        #checkbounds
        if self.type == 0 or self.type == 2:
            if self.rect.left < game.arena.left:
                self.move[0] = abs(self.move[0])
            if self.rect.right > game.arena.right:
                self.move[0] = -abs(self.move[0])
        else:
            if self.rect.top < game.arena.top:
                self.move[1] = abs(self.move[1])
            if self.rect.bottom > game.arena.bottom:
                self.move[1] = -abs(self.move[1])

        if self.bullets and self.openstate < 3:
            self.time += speedadjust * .6
            if self.openstate == 0: #start open
                self.time = 1.0
                self.frame = 1
                self.openstate = 1
            elif self.openstate == 1: #keep opening
                if self.time > openframes:
                    self.openstate = 2
            else:
                if self.time >= openframes + shootframes - 1.0:
                    if self.bullets > 1:
                        self.time -= 3.5
                    else:
                        self.openstate = 3
                    self.firenow = 1
        else:
            if self.openstate: #waiting to close
                self.time += speedadjust * .6
                if self.time >= totalframes:
                    self.openstate = 0
                    self.time = 0.0

        self.frame = int(self.time)
        if self.frame >= len(self.images):
            self.frame = 0


    def nofire(self):
        self.bullets = 0
        self.firenow = 0
        if self.openstate < openframes + shootframes:
            self.time = openframes + shootframes + 1.0


    def fire(self):
        if not self.killed:
            self.bullets += 1



class TeleGuard:
    def __init__(self, guard):
        self.guard = guard
        self.images = teleimages[guard.type]
        self.rect = self.images[0].get_rect()
        self.rect.center = guard.rect.center
        self.dead = 0
        self.time = 0.0
        self.endtime = len(self.images)*2.6

    def erase(self, background):
        r = background(self.rect)
        if self.dead:
            gfx.dirty(r)

    def draw(self, gfx):
        img = self.images[int((self.time / self.endtime) * len(self.images))]
        r = gfx.surface.blit(img, self.rect)
        gfx.dirty(r)

    def tick(self, speedadjust):
        self.time += speedadjust * 1.2
        if self.time >=  self.endtime:
            self.dead = 1
            self.guard.killed = 0
