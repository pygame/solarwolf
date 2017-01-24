# solarwolf - collecting and dodging arcade game
# Copyright (C) 2006  Pete Shinners <pete@shinners.org>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#text class

import pygame
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
        self.img, self.rect = fonts[0].text((128, 255, 255), message, availpos)
        if gfx.surface.get_bytesize() > 1:
            self.img.set_alpha(128, pygame.RLEACCEL)
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

