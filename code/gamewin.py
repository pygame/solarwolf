"gamemenu handler. main menu"

import math, os
import pygame
from pygame.locals import *
import game, gfx, snd
import gameplay, players



cheer = (
    'Congratulations!',
    'You Beat The Game!',
    ' ',
    'All Your Box Are Belong To Us',
    'Flawless Victory',
    'Your Creature Will Eat That More Often',
    'Damn! Those Alien Dastards Are Gonna Pay For Ruining My Ride',
    'Dont Shoot! I\'m With The Science Team',
    'Quad Denied', 
    'Rise From Your Grave To Save My Daughter', 
    'ChuChus aren\'t ordinary mice. We\'re space mice!', 
    'Let\'s attack agressively',
    'You dance like a monkey! Are you a monkey?',
    'Yup, That\'s a cow alright',
    'You found a chainsaw, go find some MEAT!',
    'Fight, Megaman! For everlasting peace!',
    'Tony Hawk is a Horse!',
    'Thy game is over',
    '(hey, not like the doom ending was much better)'
)


fonts = []

def load_game_resources():
    global fonts
    fontname = None
    fonts.append(pygame.font.Font(fontname, 28))
    
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



