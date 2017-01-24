#hud class

import pygame
from pygame.locals import *
import game, gfx, txt, score


hudimage = None
miniship = None
livesfont = None

def load_game_resources():
    global miniship, livesfont
    miniship = gfx.load('ship-mini-boost2.png')
    livesfont = txt.Font(None, 30)



class HUD:
    def __init__(self):
        self.imghud1 = gfx.load('hud.gif')
        self.imghud2 = gfx.load('hud2.gif')
        self.timepos = 24, 102
        self.wolfrect = Rect(16, 57, 37, 19)
        self.timesize = 64, 382
        self.timestep = self.timesize[1] / 1000.0
        self.time = 0
        self.drawsurface = gfx.surface
        self.drawoffset = 800, 0
        self.imglives = pygame.Surface((1, miniship.get_height()))
        self.imglives.set_colorkey(0, RLEACCEL)
        self.imglevel = score.render(0)
        self.poslives = 10, 510
        self.poslevel = Rect(15, 550, 1, 1) #changed later in drawlevel
        self.lastlives = 0
        self.lastlevel = 0

    def setwidth(self, width):
        width = max(min(width, 100), 0)
        oldwidth = 800 - self.drawoffset[0]
        if width == oldwidth:
            return
        self.drawsurface = gfx.surface.subsurface(800-width, 0, width, 600)
        self.drawoffset = 800-width, 0

        self.drawsurface.blit(self.imghud1, (0, 0))
        self.draw()

        gfx.surface.set_clip(0, 0, 800-width, 600)
        if oldwidth > width:
            r = game.handler.background((800-oldwidth, 0, oldwidth-width, 600))
            gfx.dirty(r)

        self.drawlives(self.lastlives, 1)
        self.drawlevel(self.lastlevel, 1)

        gfx.dirty((800-width, 0, width, 600))


    def timeheight(self, time):
        return int((1000-time) * self.timestep) + self.timepos[1]

    def drawtime(self, time):
        dest = self.drawsurface
        offset = self.drawoffset
        time = min(max(time, 0), 1000)
        if self.time == time: return
        if time > self.time:
            img = self.imghud2
            top = self.timeheight(time)
            bot = self.timeheight(self.time)
        elif time < self.time:
            img = self.imghud1
            top = self.timeheight(self.time)
            bot = self.timeheight(time)
        rect = Rect(self.timepos[0], top, self.timesize[0], bot-top)
        r = dest.blit(img, rect, rect)
        gfx.dirty(r.move(offset))
        if not self.time:
            r = dest.blit(self.imghud2, self.wolfrect, self.wolfrect)
            gfx.dirty(r.move(offset))
        elif not time:
            r = dest.blit(self.imghud1, self.wolfrect, self.wolfrect)
            gfx.dirty(r.move(offset))
        self.time = time


    def drawlives(self, lives, fast=0):
        if lives < 0: lives = 0
        dest = self.drawsurface
        offset = self.drawoffset
        if not fast:
            r = Rect(self.poslives, self.imglives.get_size())
            r2 = dest.blit(self.imghud1, r, r).move(offset)
        else:
            r2 = None
        if self.lastlives != lives:
            self.lastlives = lives
            size = miniship.get_size()
            self.imglives = pygame.Surface((size[0]*lives+1, size[1]))
            if lives <= 3: #ships
                for l in range(lives):
                    self.imglives.blit(miniship, (size[0]*l, 0))
            else: #ships and num
                self.imglives.blit(miniship, (4, 0))
                pos = size[0]+10, 0
                txt = 'x %d'%lives
                txt,pos = livesfont.text((150,200,150), txt, pos, 'topleft')
                self.imglives.blit(txt, pos)
            self.imglives.set_colorkey(0, RLEACCEL)
        r1 = dest.blit(self.imglives, self.poslives).move(offset)
        gfx.dirty2(r1, r2)


    def drawlevel(self, level, fast=0):
        dest = self.drawsurface
        offset = self.drawoffset
        if not fast:
            r = self.poslevel
            r2 = dest.blit(self.imghud1, r, r).move(offset)
        else:
            r2 = None
        if self.lastlevel != level:
            self.lastlevel = level
            self.imglevel = score.render(level)
            self.poslevel = self.imglevel.get_rect()
            self.poslevel.center = 50, 565
        r1 = dest.blit(self.imglevel, self.poslevel).move(offset)
        gfx.dirty2(r1, r2)


    def draw(self):
        if self.drawoffset[0] < 800:
            self.drawtime(game.timeleft)


