"gamemenu handler. main menu"

import math, os
import pygame
from pygame.locals import *
import game, gfx, snd, txt
import gameplay



credits = (
    ('Developer', ('Pete "ShredWheat" Shinners',)),
    ('Input Setup', ('Aaron "APS" Schlaegel',)),
    ('Music', ('"theGREENzebra"',)),
    ('Graphics Help', ('John Croisant', 'Kevin Turner', 'Michael Urman')),
    ('Special Thanks', ('David "Futility" Clark',)),
)

licenseinfo = ('This program is free software. You are encouraged to make',
               'copies and/or modify it, subject to the LGPL.',
               'See "lgpl.txt" file for details.')


fonts = []
images = []

def load_game_resources():
    global fonts, images
    fontname = None
    fonts.append((txt.Font(fontname, 25), (50, 50, 200)))
    fonts.append((txt.Font(fontname, 40), (100, 100, 250)))

    img = gfx.load('oldsolarfox.png')
    r = img.get_rect()
    r.bottomright = gfx.rect.bottomright
    images.append((img, r))

    img = gfx.load('pygame_powered.gif')
    r = img.get_rect().move(540, 20)
    images.append((img, r))

    img = gfx.load('menu_creds_on.png')
    r = img.get_rect().move(20, 5)
    images.append((img, r))

    font = txt.Font(None, 15)
    top = 560
    mid = 400
    for l in licenseinfo:
        t = font.text((50, 150, 150), l, (mid, top))
        top += t[1].height
        images.append(t)

    snd.preload('select_choose')


class GameCreds:
    def __init__(self, prevhandler):
        self.prevhandler = prevhandler
        self.done = 0
        self.top = 100
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
        t = f.text(c, text, (self.center, 0))
        t[1].top = self.top
        self.top = t[1].bottom - 5
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



