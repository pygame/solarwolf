"""Game name entry handler, part of SOLARWOLF."""
# Portions Copyright (C) 2002 Aaron "APS" Schlaegel, LGPL, see lgpl.txt

import string, math
import pygame
from pygame.locals import *
import game
import gfx, snd, txt
import input
import players
import gameplay
import gamecreds
import gamenews


charset = string.ascii_uppercase + '-.'
fontlookup = {}
fontimages = []
images = []
thefont = None
nameletters = []
stars = []

def load_game_resources():
    global menu, fontimages, boximages, thefont, charset, images, stars
    extraimgs = {'<':gfx.load('rub.gif'), '>':gfx.load('end.gif')}
    for i in extraimgs.values():
        i.set_colorkey(0, RLEACCEL)
    font = txt.Font(None, 100)
    thefont = font
    color = 120, 210, 160
    color2 = 210, 230, 220
    bgd = 0, 0, 0
    xoffset, yoffset = 75, 175
    xsize, ysize = 70, 80
    step = 0
    for letter in charset + '<>':
        pos = xoffset+xsize*(step%10), yoffset+ysize*(step//10)
        if letter in extraimgs:
            img = img2 = extraimgs[letter]
            r = img.get_rect()
            r.center = pos
        else:
            img, r = font.text(color, letter, pos)
            img2, r2 = font.text(color2, letter, pos)
        fontimages.append((img, r, letter, img2))
        step += 1
        if letter in charset:
            fontlookup[letter] = fontimages[-1]

    xoffset = 40
    for x in range(game.name_maxlength):
        rect = Rect(xoffset+x*xsize, 450, xsize, 100)
        rect2 = Rect(rect.left+1, rect.bottom-15, rect.width-2, 8)
        nameletters.append([rect, rect2, None])

    font = txt.Font(None, 40)
    img = font.render('Enter Your Name:', 1, (220, 210, 180), bgd).convert()
    img.set_colorkey(bgd, RLEACCEL)
    r = img.get_rect()
    r.center = gfx.rect.centerx, 70
    images.append((img, r))

    img = gfx.load('star.gif')
    starsize = img.get_rect()
    tmpstars = []
    for x in range(1, 12*6+2, 12):
        tmp=pygame.transform.rotate(img, x)
        tmpstars.append(tmp)
        starsize.union_ip(tmp.get_rect())
    for s in tmpstars:
        star = pygame.Surface(starsize.size)
        r = s.get_rect()
        r.center = star.get_rect().center
        star.blit(s, r)
        star.set_colorkey(s.get_colorkey(), RLEACCEL)
        stars.append(star)

    snd.preload('select_choose', 'select_move', 'incorrect', 'delete')




class GameName:
    def __init__(self, prevhandler):
        self.prevhandler = prevhandler
        self.fontimages = fontimages
        self.images = images
        self.stars = stars
        self.starrect = self.stars[0].get_rect()
        self.starframe = 0
        self.starinc = 1
        if game.clock.get_fps() < 28:
            self.starinc = 0
        self.letter = fontimages[0]
        self.selectletter(self.letter)
        self.done = 0
        if game.player:
            self.prevname = game.player.name
            game.player.name = ''
        else:
            self.prevname = ''
            game.player = players.Player('')
        for l in nameletters:
            l[2] = None
        self.step = 0.0


    def quit(self):
        snd.play('select_choose')
        game.handler = self.prevhandler
        self.done = 1
        if not game.player.name:
            game.player.name = 'NONAME'
        game.player.newguid()


    def drawletter(self, letter, lit):
        index = (0, 3)[letter==lit]
        rect = letter[1]
        gfx.surface.blit(letter[index], rect)
        gfx.dirty(rect)

    def clearletter(self, letter, lit):
        rect = letter[1]
        self.background(rect)
        if letter == lit:
            r = self.background(self.starrect)
            gfx.dirty(r)

    def selectletter(self, letter):
        self.clearletter(self.letter, self.letter)
        self.starrect.center = letter[1].center
        self.letter = letter

    def addletter(self, letter):
        if len(game.player.name) >= game.name_maxlength or letter not in charset:
            snd.play('incorrect')
            return
        snd.play('select_choose')
        game.player.name += letter
        self.recalcname()
        self.starinc = -self.starinc


    def rub(self):
        if game.player.name:
            game.player.name = game.player.name[:-1]
        self.recalcname()
        snd.play('delete')
        self.starinc = -self.starinc


    def recalcname(self):
        length = len(game.player.name)
        for x in range(game.name_maxlength):
            l = nameletters[x]
            r = self.background(l[0])
            gfx.dirty(r)
            if x < length:
                if not l[2]:
                    l[2] = thefont.render(game.player.name[x], 1, (200, 250, 200), (0, 0, 0)).convert()
                    l[2].set_colorkey((0, 0, 0), RLEACCEL)
            else:
                l[2] = None


    def drawname(self):
        hicolor = (int((math.sin(self.step)+1)*50+80),)*3
        locolor = 50, 50, 50
        lolocolor = 25, 25, 25
        curletter = len(game.player.name)
        for x in range(game.name_maxlength):
            l = nameletters[x]
            col = (x == curletter) and hicolor or locolor
            if l[2]: col = lolocolor
            r = gfx.surface.fill(col, l[1])
            gfx.dirty(r)
            if l[2]:
                r = l[2].get_rect()
                r.centerx = l[0].centerx
                r.bottom = l[0].bottom
                r = gfx.surface.blit(l[2], r)
                gfx.dirty(r)


    def input(self, i):
        if i.release:
            return
        if i.type == KEYDOWN:
            if i.unicode and i.unicode.upper() in charset:
                return
            elif i.key in (K_DELETE, K_BACKSPACE, K_RETURN, K_KP_ENTER):
                return
        if i.translated == input.ABORT:
            return self.quit()
        if i.translated == input.PRESS:
            letter = self.letter[2]
            if letter == '<':
                self.rub()
            elif letter == '>':
                self.quit()
            else:
                self.addletter(self.letter[2])
            return
        change = 0
        if i.translated == input.LEFT: change = -1
        elif i.translated == input.RIGHT: change = 1
        elif i.translated == input.UP: change = -10
        elif i.translated == input.DOWN: change = 10
        if not change:
            return
        snd.play('select_move')
        current = self.fontimages.index(self.letter) + change
        if current < 0:
            current = len(self.fontimages) + current
        if current >= len(self.fontimages):
            current = current - len(self.fontimages)
        self.selectletter(self.fontimages[current])


    def event(self, e):
        if e.type == KEYDOWN:
            if e.key in (K_DELETE, K_BACKSPACE):
                self.rub()
                self.selectletter(self.fontimages[-2])
            elif e.key in (K_RETURN, K_KP_ENTER):
                self.quit()
            elif e.unicode:
                l = e.unicode.upper()
                if l in charset:
                    self.selectletter(fontlookup[l])
                    self.addletter(l)


    def run(self):
        self.step += 0.5
        self.starframe = (self.starframe + self.starinc) % 5

        if not self.done:
            self.clearletter(self.letter, self.letter)
        else:
            for img in self.fontimages:
                self.clearletter(img, self.letter)

        gfx.updatestars(self.background, gfx)

        if not self.done:
            r = gfx.surface.blit(self.stars[int(self.starframe)], self.starrect)
            gfx.dirty(r)
            for img in self.fontimages:
                self.drawletter(img, self.letter)
            for img in self.images:
                r = gfx.surface.blit(img[0], img[1])
                gfx.dirty(r)
            self.drawname()
        else:
            for img in self.fontimages:
                gfx.dirty(img[1])
            for img in self.images:
                r = self.background(img[1])
                gfx.dirty(r)
            self.recalcname()

    def background(self, area):
        return gfx.surface.fill((0, 0, 0), area)

