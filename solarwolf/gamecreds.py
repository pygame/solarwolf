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

"gamecreds handler. who's behind this game"

import math
import pygame
import game, gfx, snd, txt



credits = (
    ('Developer', ('Pete "ShredWheat" Shinners',)),
    ('Graphics', ('Eero "Oak" Tamminen',)),
    ('Music', ('"theGREENzebra"',)),
    ('Programming Help', ('Daniel Watkins', 'Michael Witten', 'Johannes Krude', 'Aaron "APS" Schlaegel', 'Michael "MU" Urman')),
    ('Special Thanks', ('David "Futility" Clark', 'Shandy Brown', 'John "Jacius" Croisant', 'Guido "Python" van Rossum', 'Sam "SDL" Lantinga')),
)

licenseinfo = ('This program is free software. You are encouraged to',
               'make copies and modify it, subject to the LGPL.',
               'See "lgpl.txt" file for details.')


fonts = []
images = []

def load_game_resources():
    global fonts, images
    fontname = None
    fonts.append((txt.Font(fontname, 30), (50, 120, 100)))
    fonts.append((txt.Font(fontname, 44), (100, 100, 250)))

    img = gfx.load('oldsolarfox.png')
    r = img.get_rect()
    r.bottomright = gfx.rect.bottomright
    images.append((img, r))

    img = gfx.load('pygame_powered.gif')
    r = img.get_rect().move(540, 20)
    images.append((img, r))

    img = gfx.load('sdlpowered.png')
    r = img.get_rect().move(630, 150)
    images.append((img, r))

    img = gfx.load('pythonpowered.gif')
    r = img.get_rect().move(650, 280)
    images.append((img, r))

    img = gfx.load('menu_creds_on.png')
    r = img.get_rect().move(20, 5)
    images.append((img, r))

    font = txt.Font(None, 15)
    top = 560
    mid = 400
    for l in licenseinfo:
        t = font.text((50, 150, 150), l, (mid, top))
        top += t[1].height
        images.append(t)

    snd.preload('select_choose')


class GameCreds:
    def __init__(self, prevhandler):
        self.prevhandler = prevhandler
        self.done = 0
        self.center = gfx.rect.centerx - 120
        self.text = []
        self.credits = []
        self.area = pygame.Rect(40, 140, 500, 400)
        self.offset = 0
        for cred in credits:
            self.createtext(cred[0], 0)
            for peop in cred[1]:
                self.createtext(peop, 1)
            self.offset += 30
        self.offset = 0.0
        self.oldoffsety = 0.0
        self.text.extend(images)
        self.first = 1
        self.fade = ((1, 4), (8, 3), (15, 2), (21, 1))
        self.darkpic = pygame.Surface(self.area.size)
        self.darkpic.set_alpha(3)

    def createtext(self, text, size):
        f, c = fonts[size]
        t = f.textlined(c, text, (self.center, 0))
        t[1].top = self.offset
        self.offset = t[1].bottom - 5
        self.credits.append(t)


    def quit(self):
        gfx.dirty(self.background(gfx.rect))
        game.handler = self.prevhandler
        self.done = 1
        snd.play('select_choose')


    def input(self, i):
        self.quit()

    def event(self, e):
        pass


    def run(self):
        if self.first:
            gfx.dirty(gfx.rect)
            self.first = 0
        ratio = game.clockticks / 25
        speedadjust = max(ratio, 1.0)

        self.offset += speedadjust * 1.0
        offsety = self.area.bottom-self.offset

        oldclip = gfx.surface.get_clip()


        gfx.surface.blit(self.darkpic, self.area)

        gfx.updatestars(self.background, gfx)

        item = 0.0
        if not self.done:
            for cred, pos in self.text:
                gfx.surface.blit(cred, pos)
            gfx.surface.set_clip(self.area)
            for cred, pos in self.credits:
                offsetx = math.cos(self.offset * .04 + item)*30.0
                item -= 0.25
                r = pos.move(offsetx, offsety)
                bottom = r.bottom
                gfx.surface.blit(cred, r)
                #gfx.dirty(gfx.surface.blit(cred, r))
            gfx.surface.set_clip(oldclip)
            gfx.dirty(self.area)

            for y,h in self.fade:
                r = pygame.Rect(self.area.left, self.area.top+y, self.area.width, h)
                self.background(r)
                r = pygame.Rect(self.area.left, self.area.bottom-y-h, self.area.width, h)
                self.background(r)

            if bottom < self.area.top:
                self.offset = 0.0

        else:
            for text in self.text:
                r = text[1]
                gfx.dirty(self.background(text[1]))

    def background(self, area):
        return gfx.surface.fill((0, 0, 0), area)



