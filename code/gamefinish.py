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

"gamefinish handler. just lets our stars trickle"

import pygame
import gfx, game, snd



class GameFinish:
    def __init__(self, prevhandler):
        self.prevhandler = prevhandler
        self.ticks = 17
        self.started = 0

    def input(self, i):
        pass

    def event(self, e):
        pass

    def run(self):
        gfx.updatestars(self.background, gfx)
        self.ticks -= 1
        if not self.started:
            self.started = 1
            if snd.music:
                snd.music.fadeout(15*game.clockticks)

        if not self.ticks:
            gfx.surface.fill(0)
            pygame.display.update()
            #pygame.time.delay(200)
            game.handler = self.prevhandler


    def background(self, area):
        return gfx.surface.fill((0, 0, 0), area)



