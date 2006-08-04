"gamemenu handler. main menu"

import math, os
import pygame
from pygame.locals import *
import game, gfx, snd, txt
import gameplay, gamemenu, players



cheer = (
    'Congratulations!',
    'You Beat The Game!',
    ' ',
    'The known galaxy is once again safe',
    'from the unsightly Power Cubes blocking',
    'everyone\'s clear view of space. The',
    'deadly Guardian\'s plan of a littered skyline',
    'has been foiled by your cunning and skill.',
    '',
    'We can only hope that one day this threat',
    'never returns, or the power of the SolarWolf',
    'will once again be put to the test.',
)


fonts = []

def load_game_resources():
    global fonts
    fontname = None
    fonts.append(txt.Font(fontname, 28))
    snd.preload('select_choose')


class GameWin:
    def __init__(self, prevhandler):
        self.prevhandler = prevhandler
        self.done = 0
        self.top = 20
        self.center = gfx.rect.centerx
        self.text = []
        self.time = 0.0
        font = fonts[0]
        for line in cheer:
            img, r = font.text((250, 250, 250), line, (self.center, self.top))
            self.top += 30
            self.text.append((img, r))
        self.g = gamemenu.boximages
        self.y = gamemenu.yboximages
        self.r = gamemenu.rboximages



    def quit(self):
        if not game.player:
            game.player = players.Player("NONAME")
        players.make_winner(game.player)

        game.handler = self.prevhandler
        self.done = 1
        snd.play('select_choose')

        r = self.r[0].get_rect()
        gfx.dirty(self.background(r.move(50, 400)))
        gfx.dirty(self.background(r.move(300, 400)))
        gfx.dirty(self.background(r.move(550, 400)))


    def input(self, i):
        if self.time > 30.0:
            self.quit()

    def event(self, e):
        pass


    def run(self):
        for cred in self.text:
            r = cred[1]
            self.background(r)
            gfx.dirty(r)

        ratio = game.clockticks / 25
        speedadjust = max(ratio, 1.0)
        self.time += speedadjust

        gfx.updatestars(self.background, gfx)

        if not self.done:
            frame = int(self.time * .5) % len(self.r)
            surf = gfx.surface
            gfx.dirty(surf.blit(self.g[frame], (50, 400)))
            gfx.dirty(surf.blit(self.y[frame], (300, 400)))
            gfx.dirty(surf.blit(self.r[frame], (550, 400)))

            for cred, pos in self.text:
                gfx.surface.blit(cred, pos)


    def background(self, area):
        return gfx.surface.fill((0, 0, 0), area)



