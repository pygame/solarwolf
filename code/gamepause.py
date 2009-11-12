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

"""in game help screens"""

import pygame
import game
import gfx, txt
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
        titleimg, titlepos = fonts[1].text((255, 240, 200), title, (r.width/2, 10))
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
