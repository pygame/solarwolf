"gamemenu handler. main menu"

import math, os
import pygame
from pygame.locals import *
import game, gfx, snd
import gameplay



credits = (
    ('Developer', ('Pete Shinners',)),
    ('Quality Assurance', ('David Clark',)),
    ('Graphics Assistance', ('Kevin Turner',)),
    ('Special Thanks', ('Guido van Rossom', 'Sam Lantinga')),
)

licenseinfo = ('This program is free software. You are encouraged to make',
               'copies and/or modify it, subject to the of the LGPL.',
               'See "lgpl.txt" file for details.')


fonts = []
images = []

def load_game_resources():
    global fonts, images
    fontname = None
    fonts.append((pygame.font.Font(fontname, 25), (50, 50, 200)))
    fonts.append((pygame.font.Font(fontname, 40), (100, 100, 250)))

    img = gfx.load('oldsolarfox.png')
    r = img.get_rect()
    r.bottomright = gfx.rect.bottomright
    images.append((img, r))

    img = gfx.load('credrules.gif')
    r = img.get_rect().move(220, 20)
    images.append((img, r))

    img = gfx.load('python.gif')
    r = img.get_rect().move(620, 40)
    images.append((img, r))

    img = gfx.load('pygame.gif')
    r = img.get_rect().move(618, 140)
    images.append((img, r))

    img = gfx.load('sdl.gif')
    r = img.get_rect().move(636, 270)
    images.append((img, r))

    img = gfx.load('menu_creds_on.gif')
    r = img.get_rect().move(20, 5)
    images.append((img, r))

    font = pygame.font.Font(None, 14)
    top = 560
    mid = 400
    for l in licenseinfo:
        txt = gfx.text(font, (50, 150, 150), l, (mid, top))
        top += txt[1].height
        images.append(txt)

    
    snd.preload('select_choose')


class GameCreds:
    def __init__(self, prevhandler):
        self.prevhandler = prevhandler
        self.done = 0
        self.top = 120
        self.center = gfx.rect.centerx - 120
        self.text = []
        for cred in credits:
            self.createtext(cred[0], 0)
            for peop in cred[1]:
                self.createtext(peop, 1)
            self.top += 30
        self.text.extend(images)

    def createtext(self, text, size):
        f, c = fonts[size]
        t = gfx.text(f, c, text, (self.center, 0))
        t[1].top = self.top
        self.top = t[1].bottom
        self.text.append(t)
        

    def quit(self):
        game.handler = self.prevhandler
        self.done = 1
        snd.play('select_choose')


    def input(self, i):
        self.quit()

    def event(self, e):
        pass


    def run(self):
        for cred in self.text:
            r = cred[1]
            self.background(r)
            gfx.dirty(r)

        gfx.updatestars(self.background, gfx)

        if not self.done:
            for cred, pos in self.text:
                gfx.surface.blit(cred, pos)


    def background(self, area):
        return gfx.surface.fill((0, 0, 0), area)



