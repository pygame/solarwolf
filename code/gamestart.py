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
import levels

images = []
delimage = None
namefont = None
textfont = None
smallfont = None
lastplayer = None


def load_game_resources():
    global images, namefont, textfont, smallfont, delimage

    img = pygame.transform.rotate(gfx.load('ship-up.png'), -90)
    images.append((img, img.get_rect()))

    bgd = 0, 0, 0
    font = txt.Font(None, 50)
    t = font.text((220, 210, 180), 'Select A Player:', (gfx.rect.centerx, 30))
    images.append(t)

    namefont = txt.Font(None, 46)
    textfont = txt.Font(None, 26)
    smallfont = txt.Font(None, 16)

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
        self.current = [0, 0]
        self.buildlist()
        self.current = [0, 0]
        self.shipmovex = 40
        self.shipmovey = 16

        step = 0
        if lastplayer:
            for g in self.gamelist:
                if players.find_player(g[0]) == lastplayer:
                    self.current[0] = step
                    self.buildlist()
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

            if self.current[1] and len(self.gamelist[self.current[0]])<=2:
                self.current[1] = 0
            snd.play('select_move')
            x = self.gamelist[self.current[0]][1+self.current[1]][1].left
            y = self.gamelist[self.current[0]][1][1].top + self.current[1]* 10
            self.moveto((x, y))
            self.buildlist()

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
        clr3 = 100, 160, 255
        offsetx, offsety = 120, 110
        sizey = 85
        self.clearlist()
        self.gamelist = []
        cur = 0
        if len(players.players) < game.max_players:
            if self.current[0] == cur:
                c = clr3
            else:
                c = clr
            t = namefont.text(c, '-= New Player =-', (400, offsety), 'center')
            self.gamelist.append(('', t))
            offsety += sizey
            cur += 1
        for p in players.players:
            if gfx.surface.get_bitsize() > 8:
                img = pygame.Surface((450, 55))
            else:
                img = pygame.Surface((450, 55), 0, 32)

            if self.current[0] == cur:
                if self.current[1] == 1:
                    c = 200, 50, 50
                else:
                    c = clr3
            else:
                c = clr

            subimgs = []
            t,r = namefont.text(c, p.name)
            subimgs.append((t, (8, -4)))

            subimg, r = textfont.text(clr2, 'Level: ')
            r1 = subimg.get_rect()
            r1.bottomleft = 15, 54
            subimgs.append((subimg, r1))

            subimg = score.render(p.start_level())
            r = subimg.get_rect()
            r.bottomleft = r1.right, 52
            subimgs.append((subimg, r))

            if self.current[0] == cur:
                subimg = levels.preview(p.start_level())
                r = subimg.get_rect().move(280, 6)
                subimgs.append((subimg, r))

                if p.lives:
                    subimgs.append(smallfont.text((150,150,150), "Lives Used: %d"%p.lives,
                        (440,20), "topright", bgd=(30,30,30)))
                if p.skips:
                    subimgs.append(smallfont.text((150,150,150), "Levels Skipped: %d"%p.skips,
                        (440,34), "topright", bgd=(30,30,30)))

                #progress
                progress = pygame.Surface((5, 42))
                pct = int((p.start_level() / float(levels.maxlevels())) * 42)
                progress.fill((250, 50, 50), (0, 42-pct, 5, pct))
                r = progress.get_rect()
                pygame.draw.rect(progress, (255,255,255), (0,0,5,42), 1)
                subimgs.append((progress, r.move(272, 6)))


            if self.current[0] == cur:
                img.fill((30, 30, 30))
                s = img.get_size()
                pygame.draw.rect(img, (50, 50, 50), ((0,0),s), 1)
                subimgs.reverse()
                for sub, pos in subimgs:
                    img.blit(sub, pos)
            else:
                bgd = 0, 0, 0
                img.fill(bgd)
                subimgs.reverse()
                for sub, pos in subimgs:
                    img.blit(sub, pos)
                img.set_colorkey(bgd, RLEACCEL)
            img = img.convert()

            rect = img.get_rect().move(offsetx, offsety)

            images = [p.guid, (img, rect)]

            img2 = delimage
            rect2 = img2.get_rect().move(offsetx + 500, offsety + 20)
            images.append((img2, rect2))

            self.gamelist.append(images)
            offsety += sizey
            cur += 1


    def clearlist(self):
        for g in self.gamelist:
            for i,r in g[1:]:
                gfx.dirty(self.background(r))

    def drawlist(self):
        for g in self.gamelist:
            for b in g[1:]:
                gfx.dirty(gfx.surface.blit(*b))

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


