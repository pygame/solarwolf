#powerup class

import random
import pygame
from pygame.locals import *
import game, gfx, snd, objpopshot


images = []
origsize = 0,0

def load_game_resources():
    global images, origsize
#    for letter in 'bcdef':
#        img = gfx.load('powerup_' + letter + '.png')
#        images.append(img)
#    snd.preload('select_choose')
    for y in range(1,4):
        img = gfx.load('asteroid%d.png'%y)
        origsize = img.get_size()
        set = []
        for x in range(36):
            r = pygame.transform.rotate(img, x*10+8)
            set.append(r.convert())
        images.append(set)


class Asteroid:
    def __init__(self):
        self.speed = game.asteroidspeed
        self.colliderect = pygame.Rect((0, 0), origsize)
        self.reposition()
        self.dead = 0
        self.time = 0
        self.rotspeed = 0.2

    def reposition(self):
        self.images = images[random.randint(0, 2)]
        self.image = self.images[0]

        self.movex = random.random() * 2.0 - 1.0
        diff = 1.0 - abs(self.movex)
        self.movey = random.choice((diff, -diff))
        r = random.randint(0, 1200)
        if r < 700:
            self.pos = [float(r), 0.0]
        else:
            self.pos = [0.0, float(r - 700)]

        self.rotspeed = (random.random() + 3.0) * 0.15
        if random.random() < .5:
            self.rotspeed = -self.rotspeed

        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.rect.move_ip(-20, -20)
        self.colliderect.center = self.rect.center


    def predictrect(self):
        posx = (self.pos[0] + 10.0 * self.speed * self.movex) % 740
        posy = (self.pos[1] + 10.0 * self.speed * self.movey) % 640
        rect = pygame.Rect((0, 0), self.colliderect.size)
        rect.center = posx, posy
        rect.move_ip(-20, -20)
        return rect

    def erase(self, background):
        r = background(self.rect)
        #if self.dead:
        gfx.dirty(r)

    def draw(self, gfx):
        r = gfx.surface.blit(self.image, self.rect)
        gfx.dirty(r)

    def tick(self, speedadjust):
        self.time += speedadjust
        rot = int(self.time * self.rotspeed)
        self.image = self.images[rot % len(self.images)]

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

