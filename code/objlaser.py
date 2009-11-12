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

# laser beam effect from combustion powerup

import pygame.draw
import gfx



def load_game_resources():
    pass



class Laser:
    def __init__(self, start, end):
        self.clocks = 0.0
        self.life = 20.0
        self.dead = 0
        self.start = start
        self.end = end
        x = min(start[0], end[0]) - 4
        y = min(start[1], end[1]) - 4
        w = abs(start[0] - end[0]) + 8
        h = abs(start[1] - end[1]) + 8
        self.rect = pygame.Rect(x, y, w, h)

    def erase(self, background):
        if self.dead:
            r = background(self.rect)
            gfx.dirty(r)

    def draw(self, gfx):
        percent = 1.0 - (self.clocks / self.life)
        c1 = (percent * 0.4 + 0.2) * 255
        c2 = c1 / 4
        color = (c1, c2, c2)
        pygame.draw.line(gfx.surface, color, self.start, self.end, 3)
        gfx.dirty(self.rect)

    def tick(self, speedadjust):
        self.clocks += speedadjust
        if self.clocks >= self.life:
            self.dead = 1


