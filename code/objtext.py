#text class

import pygame
from pygame.locals import *
import game, gfx, txt

fonts = []
availpos = game.arena.centerx, 70
availpos_start = availpos
numtexts = 0

def load_game_resources():
    #load ship graphics
    global fonts
    fonts = [txt.Font('serif', 24, bold=0)]


class Text:
    def __init__(self, message):
        global availpos, numtexts
        bgd = 0, 0, 0
        self.img, self.rect = fonts[0].text((128, 255, 255), message, availpos)
        if gfx.surface.get_bytesize() > 1:
            self.img.set_alpha(128, RLEACCEL)
        self.clocks = game.text_length
        self.dead = 0
        availpos = availpos[0], availpos[1] + self.rect.height + 10
        numtexts += 1

    def __del__(self):
        global availpos, numtexts
        numtexts -= 1
        if not numtexts:
            availpos = availpos_start

    def erase(self, background):
        r = background(self.rect)
        if self.dead:
            gfx.dirty(r)

    def draw(self, gfx):
        r = gfx.surface.blit(self.img, self.rect)
        gfx.dirty(r)

    def tick(self, speedadjust):
        self.clocks -= 1
        runtime = game.text_length - self.clocks
        if runtime < 15 and gfx.surface.get_bytesize()>1:
            self.img.set_alpha(runtime*13)
        elif self.clocks < 15 :
            if self.clocks >= 0 and gfx.surface.get_bytesize()>1:
                self.img.set_alpha(self.clocks*13)
            self.dead = self.clocks <= 0

