#player ship class

import pygame
from pygame.locals import *
import game, gfx, math
from random import randint
import gameinit

class Stars:
    def __init__(self):
        stars = []
        scrwide, scrhigh = gfx.rect.size
        self.maxstars = 800
        for x in range(self.maxstars):
            val = randint(1, 3)
            color = val*40+60, val*35+50, val*22+100
            speed = -val, val
            rect = Rect(randint(0, scrwide), randint(0, scrhigh), 1, 1)
            stars.append([rect, speed, color])
        half = self.maxstars / 2
        self.stars = stars[:half], stars[half:]
        self.numstars = 50
        self.dead = 0
        self.odd = 0


    def recalc_num_stars(self, fps):
        if isinstance(game.handler, gameinit.GameInit):
            #don't change stars while loading resources
            return
        change = int((fps - 35.0) * 1.8)
        change = min(change, 12) #limit how quickly they can be added
        numstars = self.numstars + change
        numstars = max(min(numstars, self.maxstars/2), 0)
        if numstars < self.numstars:
            DIRTY, BGD = gfx.dirty, self.last_background
            for rect, vel, col in self.stars[self.odd][numstars:self.numstars]:
                DIRTY(BGD(rect))
        self.numstars = numstars
        #print 'STAR:', numstars, fps, change


    def erase_tick_draw(self, background, gfx):
        R, B = gfx.rect.bottomright
        FILL, DIRTY = gfx.surface.fill, gfx.dirty
        for s in self.stars[self.odd][:self.numstars]:
            DIRTY(background(s[0]))
        self.odd = not self.odd
        for rect, (xvel, yvel), col in self.stars[self.odd][:self.numstars]:
            rect.left = (rect.left + xvel) % R
            rect.top = (rect.top + yvel) % B
            DIRTY(FILL(col, rect))
        self.last_background = background


    def eraseall(self, background, gfx): #only on fullscreen switch
        R, B = gfx.rect.bottomright
        FILL = gfx.surface.fill
        for s in self.stars[0][:self.numstars]:
            background(s[0])
        for s in self.stars[1][:self.numstars]:
            background(s[0])

