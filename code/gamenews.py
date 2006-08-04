"gamemenu handler. main menu"

import math, os, threading, re
import pygame, pygame.font
from pygame.locals import *
import game, gfx, input, snd
import gameplay
import urllib, tempfile, shutil

images = []
fonts = []
downimgs = []
news_downloaded = 0

def load_game_resources():
    global images, fonts
    img = gfx.load('menu_news_on.gif')
    r = img.get_rect().move(10, 10)
    images.append((img, r))

    img = gfx.load('newsrules.gif')
    r = img.get_rect().move(220, 20)
    images.append((img, r))

    for i in ('download1', 'download2', 'downerror', 'newversion', 'downok'):
        img = gfx.load(i+'.gif')
        downimgs.append(img)

    fonts.append((pygame.font.Font(None, 40), (50, 50, 200)))
    fonts.append((pygame.font.Font(None, 26), (100, 100, 250)))
    fonts.append((pygame.font.Font(None, 30), (100, 100, 250)))
    #fonts[0][0].set_underline(1)  #this crashes SDL_ttf :[
    fonts[1][0].set_italic(1)

    snd.preload('select_choose', 'startlife', 'levelskip')


def downloadfunc(gamenews):
    global news_downloaded
    try:
        news = urllib.urlopen(game.news_url).readlines()
    except:
        gamenews.downcur = 3
        return
    gamenews.downcur = 0
    try:
        tag = re.compile('<.*>\n*')
        newsfilename = game.make_dataname('news')
        f = open(newsfilename, 'w')
        for line in news:
            l = re.sub(tag, '', line)
            if l:
                f.write(l.rstrip() + os.linesep)
        f.close()
        gamenews.success = 1
        news_downloaded = 1
    except (IOError, OSError):
        gamenews.downcur = 3



class GameNews:
    def __init__(self, prevhandler):
        global news_downloaded
        news_downloaded = 0
        self.prevhandler = prevhandler
        self.images = images
        self.imgs = []
        self.thread = None
        self.done = 1
        self.newsversion = "0.0"
        self.loadnews()
        self.done = 0
        self.success = 0
        self.downimgs = downimgs
        self.downloadpos = 600, 20
        self.clocks = 0
        self.downcur = 0
        self.lastdownrect = None

    def quit(self):
        snd.play('select_choose')
        game.handler = self.prevhandler
        self.done = 1


    def makebadnews(self, title, message):
        t = gfx.text(fonts[1][0], fonts[1][1], title, (100, 200), 'topleft')
        self.imgs.append(t)
        t = gfx.text(fonts[0][0], fonts[1][1], message, (140, 235), 'topleft')
        self.imgs.append(t)


    def rendertext(self, font, text):
        return gfx.text(fonts[font][0], fonts[font][1], text)


    def loadnews(self):
        if not self.done:
            self.cleartext()
        self.imgs = []
        newsfilename = game.make_dataname('news')
        if os.path.isfile(newsfilename):
            news = open(newsfilename).readlines()
            self.newsversion = news[0].split()[-1]
            newsitems = []
            title = date = None
            body = []
            for line in news[2:]:
                line = line.rstrip()
                if not line:
                    if title: newsitems.append((title, date, body))
                    title = date = None
                    body = []
                elif not title: title = line
                elif not date: date = line
                else: body.append(line)
            top = 140
            for t, d, body in newsitems:
                text, r = self.rendertext(0, t)
                trect = r.move(100, top)
                self.imgs.append((text, trect))
                text, r = self.rendertext(1, d)
                r = r.move(trect.right + 25, top+10)
                self.imgs.append((text, r))
                top = trect.bottom
                for b in body:
                    text, r = self.rendertext(2, b)
                    r = r.move((120, top))
                    top = r.bottom
                    self.imgs.append((text, r))
                top += 30
        else:
            self.makebadnews('Error', 'No Local Newsfile')


    def download_start(self):
        if not self.thread:
            self.success = 0
            thread = threading.Thread(None, downloadfunc, 'FETCHNEWS', [self])
            self.downcur = 1
            thread.start()
            self.thread = thread
            snd.play('startlife')


    def download_finished(self):
        self.thread = None
        snd.play('levelskip')
        self.loadnews()


    def input(self, i):
        if i == input.RIGHT:
            self.download_start()
        else:
            self.quit()

    def event(self, e):
        pass

    def cleartext(self):
        for i in self.imgs:
            r = i[1]
            self.background(r)
            gfx.dirty(r)


    def run(self):
        self.clocks += 1
        self.cleartext()

        if self.thread and (not self.thread.isAlive() and self.success):
            self.download_finished()

        clearme = None
        if self.lastdownrect:
            gfx.dirty(self.background(self.lastdownrect))
            clearme = self.lastdownrect
            self.lastdownrect = None

        gfx.updatestars(self.background, gfx)

        if not self.done:
            for img, r in self.images:
                gfx.dirty(gfx.surface.blit(img, r))
            downimg, downrect = self.downimg()
            if downimg:
                self.lastdownrect = gfx.surface.blit(downimg, downrect)
                gfx.dirty2(self.lastdownrect, clearme)
                
        else:
            for img, r in self.images:
                gfx.dirty(self.background(r))
            gfx.dirty(clearme)

        if not self.done:
            for text, pos in self.imgs:
                gfx.surface.blit(text, pos)


    def downimg(self):
        if not self.downcur:
            if self.newsversion > game.version:
                img = self.downimgs[3]
                r = img.get_rect()
                r.centerx = self.downloadpos[0]
                r.top = self.downloadpos[1]
                return img, r
            elif news_downloaded:
                img = self.downimgs[4]
                r = img.get_rect().move(self.downloadpos)
                return img, r
            else:
                return None, None
        if self.downcur == 3:
            img = self.downimgs[2]
        else:
            self.downcur = (self.clocks / 8) % 2 + 1
            img = self.downimgs[self.downcur-1]
        return img, img.get_rect().move(self.downloadpos)


    def background(self, area):
        return gfx.surface.fill((0, 0, 0), area)



