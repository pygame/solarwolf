#player ship class

import pygame
from pygame.locals import *
import game, gfx

shipimages = []
shieldimages = []

def load_game_resources():
    #load ship graphics
    global shipimages
    img = gfx.load('ship.gif')
    shipimages.append(img)
    for i in range(90, 271, 90):
        img2 = pygame.transform.rotate(img, i)
        shipimages.append(img2)
    img = gfx.load('shipon.gif')
    shipimages.append(img)
    for i in range(90, 271, 90):
        img2 = pygame.transform.rotate(img, i)
        shipimages.append(img2)
    img = gfx.load('tele_in-05.gif')
    shieldimages.append(img)
    for i in range(90, 271, 90):
        img2 = pygame.transform.rotate(img, i)
        shieldimages.append(img2)



class Ship:
    def __init__(self):
        self.move = [0, 0]
        self.turbo = 0
        self.image = 0
        self.rect = shipimages[0].get_rect()
        self.lastrect = None
        self.dead = 0
        self.active = 0
        self.speeds = game.ship_slowspeed, game.ship_fastspeed
        self.pos = list(self.rect.topleft)
        self.shield = 0

    def start(self, pos):
        self.rect.center = pos
        self.pos = list(self.rect.topleft)
        self.active = 1
        self.dead = 0
        self.move = [0, 0]
        self.turbo = 0
        self.image = 0
        self.shield = 0

    def erase(self, background):
        if self.lastrect:
            background(self.lastrect)
        if self.dead:
            gfx.dirty(self.lastrect)

    def draw(self, gfx):
        if self.shield > 1:
            img = shieldimages[self.image]
        else:
            img = shipimages[self.image + (self.turbo*4)]
        gfx.surface.blit(img, self.rect)
        gfx.dirty2(self.rect, self.lastrect)
        self.lastrect = Rect(self.rect)

    def tick(self, speedadjust = 1.0):
        speed = self.speeds[self.turbo]
        if self.shield > 1:
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

    def cmd_up(self):
        self.move = [0, -1]
        self.image = 0

    def cmd_right(self):
        self.move = [1, 0]
        self.image = 3

    def cmd_down(self):
        self.move = [0, 1]
        self.image = 2

    def cmd_turbo(self, onoff):
        self.turbo = onoff
