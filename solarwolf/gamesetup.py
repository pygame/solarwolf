"""Gamename input setup handler, part of SOLARWOLF."""
# Copyright (C) 2002 Aaron "APS" Schlaegel, LGPL, see lgpl.txt
import string, math
import pygame
from pygame.locals import *
import game
import gfx, snd, txt
import input
import score
import gameplay


images = []
delimage = None
addimage = None
allimage = None
namefont = None
namefontheight = None
textfont = None
textfontheight = None

# ship direction constants
SHIPUP    = 1
SHIPDOWN  = 2
SHIPRIGHT = 3
SHIPLEFT  = 4

DONE     = 0
BUTTONS  = 1
DELETING = 2
ADDING   = 3

def load_game_resources():
    global images, namefont, namefontheight, textfont, textfontheight, delimage, addimage, allimage
    img = pygame.transform.rotate(gfx.load('ship-up.png'), -90)
    images.append((img, img.get_rect()))

    bgd = 0, 0, 0
    font = txt.Font(None, 50)
    t = font.text((220, 210, 180), 'Setup Controls', (gfx.rect.centerx, 30))
    images.append(t)
    t = txt.Font('sans', 12).text((180, 220, 180), '(You can Pause the game with the PAUSE or P buttons)', (400, 590))
    images.append(t)

    namefontheight = 46
    namefont = txt.Font(None, 46)
    textfontheight = 26
    textfont = txt.Font(None, textfontheight)
    smallfont = txt.Font('sans', 12)

    snd.preload('select_choose', 'select_move', 'incorrect', 'delete')

    delimage = gfx.load('btn-delete.gif')
    addimage = gfx.load('btn-add.gif')
    #allimage = gfx.load('btn-all.gif')


class GameSetup:
    def __init__(self, prevhandler):
        self.prevhandler = prevhandler
        self.images = images
        self.inputstate = BUTTONS
        self.buttonlist = []
        self.buildbuttonlist()
        self.controlrectlist = []
        self.buildcontrolrectlist()
        self.actionlist = []
        self.clearactionlist()
        self.buildactionlist()
        self.currentaction = 0
        self.currentbutton = 0
        self.shipmovex = 40
        self.shipmovey = 16
        self.shipdir = SHIPRIGHT
        self.status = '...'
        self.statusimage = None
        self.buildstatus()

        self.moveto(self.targetbutton())

    def moveto(self, pos):
        if self.shipdir == SHIPUP:
            self.shippos = pos[0] - (self.images[0][1].width // 2), pos[1]
        elif self.shipdir == SHIPDOWN:
            self.shippos = pos[0] - (self.images[0][1].width // 2), pos[1] - self.images[0][1].height
        elif self.shipdir == SHIPRIGHT:
            self.shippos = pos[0] - self.images[0][1].width, pos[1] - (self.images[0][1].height // 2)
        else:
            self.shippos == pos[0], pos[1] - (self.images[0][1].height // 2)

    def displayevent(self, i):
        if i.normalized != None:
            msg = input.input_text(i.type, i.normalized)
            if msg not in (self.status, None):
                self.status = msg
                self.clearstatus()
                self.buildstatus()
                self.drawstatus()


    def quit(self):
        self.inputstate = DONE
        self.clearactionlist()
        self.clearstatus()
        snd.play('select_choose')

    def add(self, i):
        if not i.release:
            if i.all:
                snd.play('select_choose')
                self.clearactionlist()
                self.display[input.actions_order[self.currentaction]].append((i.type, i.normalized))
                input.setdisplay(self.display)
                self.buildactionlist()
                self.drawactionlist()
            else:
                snd.play('incorrect')
            self.inputstate = BUTTONS
            self.moveto(self.targetbutton())

    def delete(self):
        snd.play('delete')
        self.clearactionlist()
        del self.display[input.actions_order[self.currentaction]][self.currentcontrol]
        input.setdisplay(self.display)
        self.buildactionlist()
        self.drawactionlist()
        self.inputstate = BUTTONS
        self.moveto(self.targetbutton())

    def selectdelete(self):
        def ignoreall(x):
            return x[0] != NOEVENT
        mutable = len(list(filter(ignoreall, self.display[input.actions_order[self.currentaction]])))
        if mutable > 1:
            snd.play('select_choose')
            self.inputstate = DELETING
            self.currentcontrol = 0
            self.moveto(self.targetcontrol())
        else:
            snd.play('incorrect')

    def selectadd(self):
        if len(self.display[input.actions_order[self.currentaction]]) <= 12:
            snd.play('select_choose')
            self.inputstate = ADDING
            self.currentcontrol = len(self.display[input.actions_order[self.currentaction]])
            self.moveto(self.targetcontrol())
        else:
            snd.play('incorrect')

    def selectall(self):
        snd.play('select_choose')
        self.clearactionlist()
        if NOEVENT not in input.translations:
            input.translations[NOEVENT] = {}
        input.translations[NOEVENT][KEYDOWN] = input.actions_order[self.currentaction]
        input.translations[NOEVENT][JOYBUTTONDOWN] = input.actions_order[self.currentaction]
        self.display = input.getdisplay()
        self.buildactionlist()
        self.drawactionlist()
        self.inputstate = BUTTONS
        self.moveto(self.targetbutton())


    def input(self, i):
        if i.release:
            return
        if self.inputstate == DONE:
            return
        self.displayevent(i)

        #APS switch done to the inputstate
        if self.inputstate == BUTTONS:
            if i.translated == input.ABORT:
                self.quit()
            if i.translated == input.PRESS:
                if self.currentbutton == 0:
                    self.selectadd()
                #elif self.currentbutton == 1:
                #    self.selectall()
                else:
                    self.selectdelete()
            if i.translated in ( input.DOWN, input.UP, input.LEFT, input.RIGHT):
                if i.translated == input.DOWN:
                    self.currentaction = (self.currentaction + 1) % len(self.actionlist)
                elif i.translated == input.UP:
                    self.currentaction = (self.currentaction - 1) % len(self.actionlist)
                elif i.translated == input.LEFT:
                    self.currentbutton = (self.currentbutton - 1) % len(self.buttonlist)
                elif i.translated == input.RIGHT:
                    self.currentbutton = (self.currentbutton + 1) % len(self.buttonlist)
                snd.play('select_move')
                self.moveto(self.targetbutton())
        elif self.inputstate == DELETING:
            if i.translated == input.ABORT:
                snd.play('select_choose')
                self.inputstate = BUTTONS
                self.moveto(self.targetbutton())
            if i.translated == input.PRESS:
                self.delete()
            if i.translated in ( input.DOWN, input.UP, input.LEFT, input.RIGHT):
                if i.translated == input.DOWN or i.translated == input.UP:
                    currentcontrol = (self.currentcontrol + 6) % 12
                    if currentcontrol < len(self.display[input.actions_order[self.currentaction]]):
                        self.currentcontrol = currentcontrol
                elif i.translated == input.LEFT:
                    self.currentcontrol = (self.currentcontrol - 1) % 6 + 6 * (self.currentcontrol // 6)
                    if self.currentcontrol >= len(self.display[input.actions_order[self.currentaction]]):
                        self.currentcontrol = len(self.display[input.actions_order[self.currentaction]]) - 1
                elif i.translated == input.RIGHT:
                    self.currentcontrol = (self.currentcontrol + 1) % 6 + 6 * (self.currentcontrol // 6)
                    if self.currentcontrol >= len(self.display[input.actions_order[self.currentaction]]):
                        self.currentcontrol = 6 * (self.currentcontrol // 6)
                snd.play('select_move')
                self.moveto(self.targetcontrol())
            pass
        elif self.inputstate == ADDING:
            self.add(i)

    def targetbutton(self):
        x = self.buttonlist[self.currentbutton][1].left
        y = self.actionlist[self.currentaction][1].top + self.buttonlist[self.currentbutton][1].centery
        return (x,y)

    def targetcontrol(self):
        x = self.controlrectlist[self.currentcontrol].left
        y = self.actionlist[self.currentaction][1].top + self.controlrectlist[self.currentcontrol].centery
        return (x,y)

    def event(self, e):
        pass

    def run(self):
        r = self.background(self.images[0][1])
        gfx.dirty(r)

        self.moveship()
        gfx.updatestars(self.background, gfx)

        if self.inputstate != DONE:
            self.drawactionlist()
            self.drawstatus()
            for img in self.images:
                r = gfx.surface.blit(img[0], img[1])
                gfx.dirty(r)
        else:
            self.clearactionlist()
            self.clearstatus()
            game.handler = self.prevhandler

            for img in self.images[1:]:
                r = self.background(img[1])
                gfx.dirty(r)

    def buildcontrolrectlist(self):
        global textfontheight
        for l in range(16):
            x = 90 + 100 * (l % 6)
            y = 36 + 22 * (l // 6)
            w = 100
            h = textfontheight
            r = pygame.Rect(x, y, w, h)
            self.controlrectlist.append(r)

    def buildbuttonlist(self):
        i = 0
        #for img in (addimage, allimage, delimage):
        for img in (addimage, delimage):
            rect = img.get_rect().move(300 + 250 * i, 10)
            self.buttonlist.append((img, rect))
            i += 1


    def buildactionlist(self):
        clr = 160, 200, 250
        clr2 = 200, 200, 200
        offsety = 90
        sizey = 75
        sizex = 800
        self.actionlist = []
        self.display = input.getdisplay()
        for a in input.actions_order:
            if gfx.surface.get_bitsize() > 8:
                img = pygame.Surface((sizex, sizey))
            else:
                img = pygame.Surface((sizex, sizey), 0, 32)

            subimgs = []

            subimgs.append((namefont.render(input.actions_text[a], 1, clr), (80, 0)))

            for l in range(len(self.display[a])):
                text = input.input_text(self.display[a][l][0],self.display[a][l][1])
                subimg = textfont.render(text, 1, clr2)
                r = subimg.get_rect()
                r.topleft = self.controlrectlist[l].topleft
                subimgs.append((subimg, r))

            for b in self.buttonlist:
                subimgs.append(b)

            bgd = 0, 0, 0
            img.fill(bgd)
            for sub, pos in subimgs:
                img.blit(sub, pos)
            img.set_colorkey(bgd, RLEACCEL)
            #img = img.convert()
            rect = img.get_rect().move(0, offsety)

            self.actionlist.append((img, rect))
            offsety += sizey


    def clearactionlist(self):
        for g in self.actionlist:
            self.background(g[1])
            gfx.dirty(g[1])

    def drawactionlist(self):
        for g in self.actionlist:
            r = gfx.surface.blit(g[0], g[1])
            gfx.dirty(r)

    def buildstatus(self):
        if self.status != '...':
            statustext = "(Latest Input Event: %s)" % self.status
            self.statusimage = textfont.text((255, 250, 160), statustext, (gfx.rect.centerx, 560))
        else:
            self.statusimage = None

    def drawstatus(self):
        if self.statusimage:
            r = gfx.surface.blit(self.statusimage[0], self.statusimage[1])
            gfx.dirty(r)

    def clearstatus(self):
        if self.statusimage:
            r = self.background(self.statusimage[1])
            gfx.dirty(r)

    def background(self, area):
        return gfx.surface.fill((0, 0, 0), area)

    def moveship(self):
        pos = list(self.images[0][1].topleft)
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

        self.images[0][1].topleft = pos


