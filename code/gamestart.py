"""Game start and user select handler, part of SOLARWOLF."""

import string, math
import pygame
from pygame.locals import *
import game
import gfx, txt, snd
import input
import players
import score
import gameplay


images = []
delimage = None
namefont = None
textfont = None

lastplayer = None


def load_game_resources():
    global images, namefont, textfont, delimage

    img = pygame.transform.rotate(gfx.load('ship-up.png'), -90)
    images.append((img, img.get_rect()))

    bgd = 0, 0, 0
    font = txt.Font(None, 50)
    t = font.text((220, 210, 180), 'Select A Player:', (gfx.rect.centerx, 30))
    images.append(t)

    namefont = txt.Font(None, 46)
    textfont = txt.Font(None, 26)

    snd.preload('select_choose', 'select_move', 'delete')

    delimage = gfx.load('btn-delete.gif')


def preGameStart(prevhandler):
    if not players.players:
        game.player = players.Player('')
        return gameplay.GamePlay(prevhandler)
    else:
        return GameStart(prevhandler)


class GameStart:
    def __init__(self, prevhandler):
        self.prevhandler = prevhandler
        self.images = images
        self.done = 0
        self.aborted = 0
        self.gamelist = []
        self.buildlist()
        self.current = [0, 0]
        self.shipmovex = 40
        self.shipmovey = 16

        step = 0
        if lastplayer:
            for g in self.gamelist:
                if players.find_player(g[0]) == lastplayer:
                    self.current[0] = step
                step += 1

        self.moveto(self.gamelist[self.current[0]][1][1])



    def starting(self):
        #snd.playmusic('gamestart.wav')
        pass


    def moveto(self, pos):
        self.shippos = pos[0] - 10, pos[1] + 10


    def input(self, i):
        if self.done:
            return
        if i.release:
            return
        if i.translated == input.ABORT:
            self.aborted = 1
            self.done = 1
            self.current[0] = -1
            self.clearlist()
            self.moveto((2, 2))
            snd.play('select_choose')
        if i.translated == input.PRESS:
            return self.pressed()

        if i.translated in ( input.DOWN, input.UP, input.LEFT, input.RIGHT):
            if i.translated == input.DOWN:
                self.current[0] = (self.current[0] + 1) % len(self.gamelist)
            elif i.translated == input.UP:
                self.current[0] = (self.current[0] - 1) % len(self.gamelist)
            elif i.translated == input.LEFT or i.translated == input.RIGHT:
                self.current[1] = not self.current[1]

            if self.current[1] and not self.gamelist[self.current[0]][2]:
                self.current[1] = 0
            snd.play('select_move')
            x = self.gamelist[self.current[0]][1+self.current[1]][1].left
            y = self.gamelist[self.current[0]][1][1].top + self.current[1]* 24
            self.moveto((x, y))

    def event(self, e):
        pass

    def run(self):
        r = self.background(self.images[0][1])
        gfx.dirty(r)

        self.moveship()
        gfx.updatestars(self.background, gfx)

        if not self.done:
            self.drawlist()
            for img in self.images:
                r = gfx.surface.blit(img[0], img[1])
                gfx.dirty(r)
        else:
            if gfx.rect.colliderect(self.images[0][1]) and not self.aborted:
                if self.current[0] >= 0:
                    g = self.gamelist[self.current[0]]
                    r = gfx.surface.blit(g[1][0], g[1][1])
                    gfx.dirty(r)
                for img in self.images:
                    r = gfx.surface.blit(img[0], img[1])
                    gfx.dirty(r)
            else:
                self.clearlist()
                if self.aborted:
                    game.handler = self.prevhandler
                else:
                    game.handler = gameplay.GamePlay(self.prevhandler)

            for img in self.images[1:]:
                r = self.background(img[1])
                gfx.dirty(r)




    def background(self, area):
        return gfx.surface.fill((0, 0, 0), area)


    def buildlist(self):
        self.clearlist()
        clr = 160, 200, 250
        clr2 = 200, 200, 200
        offsetx, offsety = 120, 110
        sizey = 85
        self.clearlist()
        self.gamelist = []
        if len(players.players) < game.max_players:
            t = namefont.text(clr, '-= New Player =-', (offsetx, offsety), 'topleft')
            self.gamelist.append(('', t, None))
            offsety += sizey
        for p in players.players:
            if gfx.surface.get_bitsize() > 8:
                img = pygame.Surface((490, 55))
            else:
                img = pygame.Surface((490, 55), 0, 32)

            subimgs = []
            t,r = namefont.text(clr, p.name)
            subimgs.append((t, (0, 0)))

            subimg, r = textfont.text(clr2, 'Level: ')
            r1 = subimg.get_rect()
            r1.bottomleft = 10, img.get_height()
            subimgs.append((subimg, r1))

            subimg = score.render(p.start_level())
            r = subimg.get_rect()
            r.bottomleft = r1.bottomright
            subimgs.append((subimg, r))

            bgd = 0, 0, 0
            img.fill(bgd)
            for sub, pos in subimgs:
                img.blit(sub, pos)
            img.set_colorkey(bgd, RLEACCEL)
            #img = img.convert()

            rect = img.get_rect().move(offsetx, offsety)
            img2 = delimage
            rect2 = img2.get_rect().move(offsetx + 500, offsety + 40)
            self.gamelist.append((p.guid, (img, rect), (img2, rect2)))
            offsety += sizey


    def clearlist(self):
        for g in self.gamelist:
            self.background(g[1][1])
            gfx.dirty(g[1][1])
            if g[2]:
                self.background(g[2][1])
                gfx.dirty(g[2][1])

    def drawlist(self):
        for g in self.gamelist:
            r = gfx.surface.blit(g[1][0], g[1][1])
            gfx.dirty(r)
            if g[2]:
                r = gfx.surface.blit(g[2][0], g[2][1])
                gfx.dirty(r)

    def moveship(self):
        pos = list(self.images[0][1].topright)
        if pos[0] + self.shipmovex < self.shippos[0]:
            pos[0] += self.shipmovex
        elif pos[0] < self.shippos[0]:
            pos[0] = self.shippos[0]

        if pos[0] - self.shipmovex > self.shippos[0]:
            pos[0] -= self.shipmovex
        elif pos[0] > self.shippos[0]:
            pos[0] = self.shippos[0]

        if pos[1] + self.shipmovey < self.shippos[1]:
            pos[1] += self.shipmovey
        elif pos[1] < self.shippos[1]:
            pos[1] = self.shippos[1]

        if pos[1] - self.shipmovey > self.shippos[1]:
            pos[1] -= self.shipmovey
        elif pos[1] > self.shippos[1]:
            pos[1] = self.shippos[1]

        self.images[0][1].topright = pos


    def pressed(self):
        g = self.gamelist[self.current[0]]
        p = players.find_player(g[0])
        if self.current[1] == 0:
            snd.play('select_choose')
            if not p:
                p = players.Player('')
            global lastplayer
            lastplayer = p
            game.player = p
            self.clearlist()
            self.moveto((860, 500))
            self.done = 1
        else:
            snd.play('delete')
            players.players.remove(p)
            self.buildlist()
            self.current = [0, 0]
            self.moveto((120, 110))


