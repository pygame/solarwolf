"gamemenu handler. main menu"

import math, os
import pygame
from pygame.locals import *
import game, gfx, snd
import gameplay



cheer = (
    'Congradulations!',
    'You Beat The Game!',
    ' ',
    'All Your Box Are Belong To Us',
    'Flawless Victory',
    'Ya Headless Freaks',
    'Your Creature Will Eat That More Often',
    'Thou Hast Gained An Eighth',
    'Stay Awhile And Listen',
    'Damn! Those alien dastards are gonna pay for ruining my ride',
    'Dont Shoot! I\'m with the science team',
    'You Spoony Bard', 
    'Quad Damage', 
    ' ', 
    ' ', 
    ' ', 
    '(hey, not like the doom ending was much better)'
)


fonts = []

def load_game_resources():
    global fonts
    fontname = None
    fonts.append(pygame.font.Font(fontname, 30))
    
    snd.preload('select_choose')


class GameWin:
    def __init__(self, prevhandler):
        self.prevhandler = prevhandler
        self.done = 0
        self.top = 50
        self.center = gfx.rect.centerx
        self.text = []
        font = fonts[0]
        for line in cheer:
            img, r = gfx.text(font, (250, 250, 250), line, (self.center, self.top))
            self.top += 30
            self.text.append((img, r))
        

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



