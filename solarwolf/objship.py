#player ship class

import pygame
from pygame.locals import *
import game, gfx

upimage = None
shieldbg = None
bulletbg = None
shipimages = []

def load_game_resources():
    #load ship graphics
    global upimage, shipimages, shieldbg, bulletbg

    upimage = gfx.load('ship-up.png')

    anim = []
    for img in gfx.animstrip(gfx.load('ship-up-boost1.png')):
        imgs = [img]
        for i in range(90, 359, 90):
            imgs.append(pygame.transform.rotate(img, i))
        anim.append(imgs)
    shipimages.extend(list(zip(*anim)))

    anim = []
    for img in gfx.animstrip(gfx.load('ship-up-boost2.png')):
        imgs = [img]
        for i in range(90, 359, 90):
            imgs.append(pygame.transform.rotate(img, i))
        anim.append(imgs)
    shipimages.extend(list(zip(*anim)))

    shieldbg = gfx.animstrip(gfx.load('bonus-shield.png'))
    bulletbg = gfx.animstrip(gfx.load('bonus-bullet.png'))


class Ship:
    def __init__(self):
        self.move = [0, 0]
        self.unmoved = 1
        self.turbo = game.thruster
        self.image = 0
        self.frame = 0.0
        self.rect = shipimages[0][0].get_rect()
        self.lastrect = None
        self.dead = 0
        self.active = 0
        self.speeds = game.ship_slowspeed, game.ship_fastspeed
        self.pos = list(self.rect.topleft)
        self.shield = 0
        self.bullet = 0

    def start(self, pos):
        self.rect.topleft = pos
        self.pos = list(self.rect.topleft)
        self.unmoved = 1
        self.active = 1
        self.dead = 0
        self.move = [0, 0]
        self.turbo = game.thruster
        self.image = 0
        self.shield = 0

    def erase(self, background):
        if self.lastrect:
            background(self.lastrect)
        if self.dead:
            gfx.dirty(self.lastrect)

    def draw(self, gfx):
        frame = int(self.frame) % 4
        if self.shield:
            gfx.surface.blit(shieldbg[self.shield-1], self.rect)
        elif self.bullet:
            gfx.surface.blit(bulletbg[self.bullet-1], self.rect)
        if self.unmoved:
            img = upimage
        else:
            img = shipimages[self.image + (self.turbo*4)][frame]
        gfx.surface.blit(img, self.rect)
        gfx.dirty2(self.rect, self.lastrect)
        self.lastrect = Rect(self.rect)

    def tick(self, speedadjust = 1.0):
        self.frame += speedadjust
        speed = self.speeds[self.turbo]
        if self.shield == 1:
            speed = int(speed * speedadjust * 1.3)
        else:
            speed = int(speed * speedadjust)
        self.pos[0] += self.move[0] * speed
        self.pos[1] += self.move[1] * speed
        self.rect.topleft = self.pos
        if self.rect.top < game.arena.top:
            self.rect.top = game.arena.top
            self.pos[1] = float(self.rect.top)
            self.move[1] = 0
        elif self.rect.bottom > game.arena.bottom:
            self.rect.bottom = game.arena.bottom
            self.pos[1] = float(self.rect.top)
            self.move[1] = 0
        if self.rect.left < game.arena.left:
            self.rect.left = game.arena.left
            self.pos[0] = float(self.rect.left)
            self.move[0] = 0
        elif self.rect.right > game.arena.right:
            self.rect.right = game.arena.right
            self.pos[0] = float(self.rect.left)
            self.move[0] = 0


    def cmd_left(self):
        self.move = [-1, 0]
        self.image = 1
        self.unmoved = 0

    def cmd_up(self):
        self.move = [0, -1]
        self.image = 0
        self.unmoved = 0

    def cmd_right(self):
        self.move = [1, 0]
        self.image = 3
        self.unmoved = 0

    def cmd_down(self):
        self.move = [0, 1]
        self.image = 2
        self.unmoved = 0

    def cmd_turbo(self, onoff):
        if game.thruster:
            onoff = not onoff
        self.turbo = onoff
