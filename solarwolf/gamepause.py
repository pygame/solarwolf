"""in game help screens"""

import math
import pygame
from pygame.locals import *
import game
import gfx, snd, txt
import input
import gamehelp

fonts = []

def load_game_resources():
    fonts.append(txt.Font('sans', 16, italic=1))
    fonts.append(txt.Font('sans', 25, bold=1))




class GamePause(gamehelp.GameHelp):
    def __init__(self, prevhandler):
        x = game.arena.centerx - 60
        y = game.arena.centery - 20
        gamehelp.GameHelp.__init__(self, prevhandler, '', (x, y))


    def drawhelp(self, name, pos):
        title = 'Paused'
        text = 'Press Any Key To Continue'

        self.img = fonts[0].textbox((255, 240, 200), text, 200, (50, 100, 50), 50)
        r = self.img.get_rect()
        titleimg, titlepos = fonts[1].text((255, 240, 200), title, (r.width//2, 10))
        self.img.blit(titleimg, titlepos)
        r.topleft = pos
        r = r.clamp(game.arena)
        alphaimg = pygame.Surface(self.img.get_size())
        alphaimg.fill((50, 100, 50))
        alphaimg.set_alpha(192)
        gfx.surface.blit(alphaimg, r)
        self.img.set_colorkey((50, 100, 50))
        self.rect = gfx.surface.blit(self.img, r)
        gfx.dirty(self.rect)
