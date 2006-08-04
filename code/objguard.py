#simple enemy class

import os
import pygame, pygame.image
from pygame.locals import *
import game, gfx

images = []
guard_anim = 0,1,2,3,4,3,4,4,5,5,5,6,5,5,6,6
guard_loadtime = len(guard_anim)

def load_game_resources():
    #load ship graphics
    global images
    imgs = []
    for i in range(0,7):
        img = gfx.load('guard_n-%02d.gif'%i)
        imgs.append(img)
    animimgs = map(lambda index, l=imgs: l[index], guard_anim)
    images.append(animimgs)
    for x in range(90, 271, 90):
        rotimgs = []
        for i in imgs:
            r = pygame.transform.rotate(i, x)
            rotimgs.append(r)
        animimgs = map(lambda index, l=rotimgs: l[index], guard_anim)
        images.append(animimgs)



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
        self.reloading = 0
        self.fireme = 0
        self.waitshots = 0
        self.pos = list(self.rect.topleft)

    def shotinfo(self):
        speed = game.shot_speed
        if self.type == 0: #top
            return (self.rect.centerx, self.rect.bottom), (0, speed)
        elif self.type == 1: #left
            return (self.rect.right, self.rect.centery), (speed, 0)
        elif self.type == 2: #bottom
            return (self.rect.centerx, self.rect.top), (0, -speed)
        else: #right
            return (self.rect.left, self.rect.centery), (-speed, 0)

    def erase(self, background):
        if self.lastrect:
            r = background(self.lastrect)
            if self.dead:
                gfx.dirty(r)

    def draw(self, gfx):
        img = self.images[0]
        if self.reloading:
            index = guard_loadtime-self.reloading
            img = self.images[index]
        gfx.surface.blit(img, self.rect)
        gfx.dirty2(self.rect, self.lastrect)
        self.lastrect = Rect(self.rect)

    def tick(self, speedadjust = 1.0):
        self.pos[0] += self.move[0] * speedadjust
        self.pos[1] += self.move[1] * speedadjust
        self.rect.topleft = self.pos
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
        if self.reloading:
            self.reloading -= 1
            self.fireme = (self.reloading == 1)
        return self.dead

