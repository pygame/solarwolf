"Game main menu handler, part of SOLARWOLF."

import math, os
import pygame, pygame.draw
from pygame.locals import *
import game
import gfx, snd, txt
import input
import players
import gamecreds, gamenews, gamestart, gamesetup

import gamewin



images = []
boximages = []
yboximages = []
rboximages = []

class MenuItem:
    def __init__(self, imgname, handler):
        self.imgname = imgname
        self.handler = handler

    def init(self, pos):
        self.img_on = gfx.load('menu_'+self.imgname+'_on.png')
        self.img_off = gfx.load('menu_'+self.imgname+'_off.png')
        self.rect = self.img_on.get_rect().move(pos)
        self.smallrect = self.img_off.get_rect()
        self.smallrect.center = self.rect.center



menu = [
    MenuItem('start', gamestart.preGameStart),
#    MenuItem('highs', gamename.GameName),
    MenuItem('news', gamenews.GameNews),
    MenuItem('creds', gamecreds.GameCreds),
    MenuItem('setup', gamesetup.GameSetup),
    MenuItem('quit', None),
]



def load_game_resources():
    global menu, images, boximages
    images = []
    pos = [20, 420] #[100, 420]
    odd = 0
    for m in menu:
        m.init(pos)
        pos[0] += 150
        odd = (odd+1)%2
        if odd:
            pos[1] += 20
        else:
            pos[1] -= 20
    images.append(gfx.load('menu_on_bgd.png'))
    images[0].set_colorkey(0)
    images.append(gfx.load('logo.png'))
    images.append(gfx.load('bigship.png'))
    images[1].set_colorkey()
    images[2].set_colorkey()
    for i in range(15):
        #boximages.append(gfx.load('bigbox%04d.gif'%i))
        img = gfx.load_raw('bigbox%04d.gif'%i)
        boximages.append(img.convert())
        pal = img.get_palette()
        newpal = [(g,g,b) for (r,g,b) in pal]
        img.set_palette(newpal)
        yboximages.append(img.convert())
        newpal = [(g,b,b) for (r,g,b) in pal]
        img.set_palette(newpal)
        rboximages.append(img.convert())

    snd.preload('select_move', 'select_choose')


class GameMenu:
    def __init__(self, prevhandler):
        self.prevhandler = prevhandler
        self.current = 0
        self.glow = 0.0
        self.switchhandler = None
        self.switchclock = 0
        self.startclock = 5
        self.logo = images[1]
        self.logorect = self.logo.get_rect().move(30, 25)
        self.logorectsmall = self.logorect.inflate(-2,-2)
        self.boxtick = 0
        if players.winners:
            self.boximages = rboximages
        else:
            self.boximages = boximages
        self.boxrect = self.boximages[0].get_rect().move(580, 80)
        self.bigship = images[2]
        self.bigshiprect = self.bigship.get_rect().move(450, 250)

        fnt = txt.Font(None, 18)
        self.version = fnt.text((100, 200, 120), 'SolarWolf Version ' + game.version, (10, 580), 'topleft')


    def starting(self):
        snd.playmusic('aster2_sw.xm')

        gfx.dirty(gfx.surface.blit(self.logo, self.logorect))
        gfx.dirty(gfx.surface.blit(self.bigship, self.bigshiprect))

        if players.winners:
            msg = 'Hall Of Famers:  '
            for w in players.winners:
                msg += w.name + '  '
            textfont = txt.Font(None, 26)
            t = textfont.text((255, 250, 160), msg, (gfx.rect.centerx, 560))
            self.fame = t
        else:
            self.fame = None

    def quit(self):
        self.current = len(menu)-1
        self.workbutton()


    def workbutton(self):
        button = menu[self.current]
        if not button.handler:
            self.switchhandler = self.prevhandler
        else:
            self.switchhandler = button.handler
        self.switchclock = 10


    def clearitem(self, item, dirty=0):
        r = self.background(item.rect)
        if dirty:
            gfx.dirty(r)


    def setalphas(self, alpha, extras=[]):
        imgs = []
        selected = menu[self.current]
        imgs.extend([x.img_off for x in menu if x is not selected])
        imgs.extend(extras)
        if gfx.surface.get_bytesize()==1:
            return
        if alpha < 255:
            for i in imgs:
                i.set_alpha(alpha)
        else:
            for i in imgs:
                i.set_alpha()
                c = i.get_colorkey()
                if c:
                    i.set_colorkey(c, RLEACCEL)


    def drawitem(self, item, lit):
        if not lit:
            gfx.surface.blit(item.img_off, item.smallrect)
        else:
            lite = images[0]
            glowval = (math.sin(self.glow) + 2.5) * 50.0
            if self.switchclock == 2:
                glowval /= 2
            if gfx.surface.get_bytesize()>1:
                lite.set_alpha(glowval)
            gfx.surface.blit(lite, item.rect)
            gfx.surface.blit(item.img_on, item.rect)
        gfx.dirty(item.rect)


    def input(self, i):
        if i.release:
            return
        if self.switchclock:
            return
        if i.translated == input.LEFT:
            self.current = (self.current - 1)%len(menu)
            snd.play('select_move')
        elif i.translated == input.RIGHT:
            self.current = (self.current + 1)%len(menu)
            snd.play('select_move')
        elif i.translated == input.PRESS:
            self.workbutton()
            snd.play('select_choose')
        elif i.translated == input.ABORT:
            snd.play('select_choose')
            self.quit()

    def event(self, e):
        pass


    def run(self):
        self.glow += .35
        self.boxtick = (self.boxtick + 1)%15
        boximg = self.boximages[self.boxtick]

        if self.startclock:
            alpha = (6-self.startclock)*40
            self.setalphas(alpha, [menu[self.current].img_on, boximg])
            self.background(self.boxrect)
        elif self.switchclock:
            alpha = (self.switchclock-1)*20
            self.setalphas(alpha, [boximg])
            self.background(self.boxrect)
            if self.switchclock == 2 and gfx.surface.get_bytesize()>1:
                menu[self.current].img_on.set_alpha(128)

        for m in menu:
            self.clearitem(m)

        gfx.updatestars(self.background, gfx)

        gfx.dirty(gfx.surface.blit(*self.version))
        if self.fame:
            gfx.dirty(gfx.surface.blit(*self.fame))

        if self.startclock == 1 or self.switchclock == 1:
            self.setalphas(255, [menu[self.current].img_on] + self.boximages)

        if self.switchclock != 1:
            r = gfx.surface.blit(boximg, self.boxrect)
            gfx.dirty(r)

            select = menu[self.current]
            for m in [m for m in menu if m is not select]:
                self.drawitem(m, 0)
            self.drawitem(select, 1)

        else:
            for m in menu:
                gfx.dirty(m.rect)
            if self.switchhandler == self.prevhandler:
                game.handler = self.prevhandler
            else:
                game.handler = self.switchhandler(self)
                self.switchclock = 0
                self.switchhandler = None
                self.startclock = 5
            if self.fame:
                gfx.dirty(self.background(self.fame[1]))
            gfx.dirty(self.background(self.version[1]))
            if self.fame:
                gfx.dirty(self.background(self.fame[1]))
            gfx.dirty(gfx.surface.fill((0, 0, 0), self.logorect))
            gfx.dirty(gfx.surface.fill((0, 0, 0), self.bigshiprect))

        if self.startclock:
            self.startclock -= 1
        elif self.switchclock:
            self.switchclock -= 1



    def background(self, area):
        fullr = gfx.surface.fill((0, 0, 0), area)
        if self.switchclock != 1:
            if area.colliderect(self.bigshiprect):
                    r = area.move(-self.bigshiprect.left, -self.bigshiprect.top)
                    return gfx.surface.blit(self.bigship, area, r)
            elif self.switchclock != 1:
                if area.colliderect(self.logorectsmall):
                    r = area.move(-self.logorect.left, -self.logorect.top)
                    return gfx.surface.blit(self.logo, area, r)
        return fullr


