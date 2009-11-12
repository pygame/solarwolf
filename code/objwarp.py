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

#jumptowarp animation class

import gfx


images = []
CLOCK_MULTIPLIER = 3.0


def load_game_resources():
    global images
    #for i in range(1,16):
    #    img = gfx.load('warp_%04d.gif'%i)
    #    images.append(img)

    images = gfx.animstrip(gfx.load('ship-warp.png'), 48)

    #~ # Hold the blank frame for a few extra counts.
    #~ images[12:] = [images[11]]*2 + [images[-1], images[-2], images[-2], images[-1]]
    #~ # Add on an extra bit of twinkle at the end.
    #~ #images.extend([images[-2],images[-2]])

    images.extend([images[-1]]*2)


class Warp:
    def __init__(self, pos):
        self.images = images
        self.numclocks = len(images)*CLOCK_MULTIPLIER
        self.clocks = 0.0
        self.rect = images[0].get_rect()
        self.rect.center = pos
        self.dead = 0
        self.lastrect = None

    def erase(self, background):
        if self.lastrect:
            r = background(self.lastrect)
            if self.dead:
                gfx.dirty(r)

    def draw(self, gfx):
        frame = min(int(self.clocks/CLOCK_MULTIPLIER), len(self.images)-1)
        img = images[frame]
        r = gfx.surface.blit(img, self.rect)
        gfx.dirty2(r, self.lastrect)
        self.lastrect = r

    def tick(self, speedadjust):
        self.clocks += speedadjust
        # Ship moves to the right until it disappears, then the
        # "twinkle" is stationary.
        if self.clocks/CLOCK_MULTIPLIER < 12:
            self.rect.left += 2
            self.rect.top -= 1
        if self.clocks >= self.numclocks:
            self.dead = 1
