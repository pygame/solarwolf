#player ship class

import pygame
from pygame.locals import *
import game, gfx

shipimages = []

def load_game_resources():
    #load ship graphics
    global shipimages
    for i in range(1,5):
        img = gfx.load('ship%d.gif'%i)
        shipimages.append(img)


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

    def start(self, pos):
        self.rect.center = pos
        self.pos = list(self.rect.topleft)
        self.active = 1
        self.dead = 0
        self.move = [0, 0]
        self.turbo = 0
        self.image = 0

    def erase(self, background):
        if self.lastrect:
            background(self.lastrect)
        if self.dead:
            gfx.dirty(self.lastrect)

    def draw(self, gfx):
        img = shipimages[self.image]
        gfx.surface.blit(img, self.rect)
        gfx.dirty2(self.rect, self.lastrect)
        self.lastrect = Rect(self.rect)

    def tick(self, speedadjust = 1.0):
        speed = self.speeds[self.turbo]
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
