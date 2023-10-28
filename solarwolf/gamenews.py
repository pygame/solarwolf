"""Game news page handler, part of SOLARWOLF."""

import math, os, threading, re
import urllib.request, urllib.parse, urllib.error, tempfile, shutil
import pygame, pygame.font
from pygame.locals import *
import game
import gfx, snd, txt
import input
import gameplay
import webbrowser
import objbox

images = []
fonts = []
downimgs = []
news_downloaded = 0
ship = None


Options = [
"Main Menu",
"Download News",
"Visit Website",
]


def load_game_resources():
    global images, fonts, downimgs, ship
    img = gfx.load('menu_news_on.png')
    r = img.get_rect().move(10, 10)
    images.append((img, r))

    img = gfx.load('download.png')
    downimgs = gfx.animstrip(img, img.get_width()//2)
    for i in ('downerror', 'newversion', 'downok'):
        img = gfx.load(i+'.gif')
        downimgs.append(img)

    fonts.append((txt.Font(None, 36, italic=1), (150, 150, 200)))
    fonts.append((txt.Font(None, 22), (120, 120, 250)))
    fonts.append((txt.Font(None, 28), (120, 120, 250)))

    ship = pygame.transform.rotate(gfx.load('ship-up.png'), -90)

    snd.preload('select_choose', 'startlife', 'levelskip')


def downloadfunc(gamenews):
    global news_downloaded
    try:
        req = urllib.request.Request(
            game.news_url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )

        f = urllib.request.urlopen(req)
        news = [n.decode('utf-8') for n in f.readlines()]
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
        self.boxes = []
        self.thread = None
        self.newsversion = "0.0"
        self.loadnews()
        self.success = 0
        self.downimgs = downimgs
        self.downloadpos = 660, 10
        self.clocks = 0
        self.downcur = 0
        self.lastdownrect = None

        self.shipimage = [ship, ship.get_rect()]

        self.done = 0
        self.aborted = 0
        self.linesize = 60
        self.current = 0
        self.gamelist = []
        self.buildlist()
        self.shipmovex = 20
        self.shipmovey = 14
        self.moveto(self.gamelist[0][1])
        self.tempwindowed = 0
        self.launchthebrowser = 0



    def starting(self):
        pass
        #self.download_start()

    def quit(self):
        if self.tempwindowed:
            game.display = 1
            gfx.switchfullscreen()
        game.handler = self.prevhandler
        self.done = 1


    def makebadnews(self, title, message):
        t = fonts[1][0].text(fonts[1][1], title, (100, 200), 'topleft')
        self.imgs.append(t)
        t = fonts[0][0].text(fonts[1][1], message, (140, 235), 'topleft')
        self.imgs.append(t)


    def rendertext(self, font, text):
        return fonts[font][0].text(fonts[font][1], text)


    def loadnews(self):
        self.cleartext()
        self.imgs = []
        self.boxes = []
        newsfilename = game.make_dataname('news')
        if not os.path.isfile(newsfilename):
            newsfilename = game.get_resource('news')
        if os.path.isfile(newsfilename):
            news = open(newsfilename).readlines()[2:]
            if not news:
                self.makebadnews(' ', 'Invalid News File')
                return
            newsparts = news[0].split()
            if not newsparts:
                self.makebadnews(' ', 'Invalid News File')
                return

            self.newsversion = newsparts[-1]
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
            top = 150
            for t, d, body in newsitems:
                self.boxes.append(objbox.Box((28, top+3), 1))
                self.boxes[-1].rotspeed = 2.0
                self.boxes[-1].rotate = 0.0
                text, r = self.rendertext(0, t)
                trect = r.move(60, top)
                self.imgs.append((text, trect))
                text, r = self.rendertext(1, d)
                r = r.move(trect.right + 25, top+10)
                self.imgs.append((text, r))
                top = trect.bottom
                for b in body:
                    text, r = self.rendertext(2, b)
                    r = r.move((100, top))
                    top = r.bottom
                    self.imgs.append((text, r))
                top += 24
        else:
            self.makebadnews(' ', 'Cannot Download News')


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


    def moveto(self, pos):
        self.shippos = pos[0], pos[1]


    def input(self, i):
        if self.done:
            return
        if i.release:
            return

        if i.translated == input.ABORT:
            self.aborted = 1
            self.done = 1
            snd.play('select_choose')
            self.quit()
        if i.translated == input.PRESS:
            return self.pressed()

        if i.translated in (input.DOWN, input.UP):
            if i.translated == input.DOWN:
                self.current = (self.current+1) % len(self.gamelist)
            else:
                self.current = (self.current-1) % len(self.gamelist)
            snd.play('select_move')
            x = self.gamelist[self.current][1].left
            y = self.gamelist[self.current][1].top
            self.moveto((x, y))
            self.buildlist()


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

        if self.thread and (not self.thread.is_alive() and self.success):
            self.download_finished()

        clearme = None
        if self.lastdownrect:
            gfx.dirty(self.background(self.lastdownrect))
            clearme = self.lastdownrect
            self.lastdownrect = None

        r = self.background(self.shipimage[1])
        gfx.dirty(r)

        gfx.updatestars(self.background, gfx)

        if not self.done:
            for img, r in self.images:
                gfx.dirty(gfx.surface.blit(img, r))
            downimg, downrect = self.downimg()
            if downimg:
                self.lastdownrect = gfx.surface.blit(downimg, downrect)
                gfx.dirty2(self.lastdownrect, clearme)

            for text, pos in self.imgs:
                gfx.surface.blit(text, pos)
        else:
            for img, r in self.images:
                gfx.dirty(self.background(r))
            gfx.dirty(clearme)

        if not self.done:
            self.drawlist()
            self.moveship()
            r = gfx.surface.blit(self.shipimage[0], self.shipimage[1])
            gfx.dirty(r)
            for b in self.boxes:
                b.erase(self.background)
                b.tick(1.0)
                b.draw(gfx)
        else:
            #game.handler = self.prevhandler
            for b in self.boxes:
                b.erase(self.background)
            self.clearlist()

        if self.launchthebrowser:
            #we do it like this so the window can get
            #unfullscreened and not minimized on windows
            self.launchthebrowser -= 1
            if not self.launchthebrowser:
                webbrowser.open(game.site_url, 1, 1)


    def downimg(self):
        if not self.downcur:
            if self.newsversion > game.version:
                img = self.downimgs[3]
                r = img.get_rect()
                r.midtop = self.downloadpos
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
            self.downcur = (self.clocks // 8) % 2 + 1
            img = self.downimgs[int(self.downcur-1)]
        return img, img.get_rect().move(self.downloadpos)


    def background(self, area):
        return gfx.surface.fill((0, 0, 0), area)


    def buildlist(self):
        clr = 220, 230, 240
        clr2 = 140, 150, 160
        offsetx, offsety = 240, 30
        self.clearlist()
        font = fonts[0][0]
        self.gamelist = []
        cur = 0
        for opt in Options:
            if self.current == cur:
                c = clr
            else:
                c = clr2
            imgpos = font.text(c, opt, (offsetx, offsety), "midleft")
            self.gamelist.append(imgpos)
            offsety += 33
            cur += 1


    def clearlist(self):
        for o in self.gamelist:
            gfx.dirty(self.background(o[1]))
        for b in self.boxes:
            b.dead = 1
            b.erase(self.background)

    def drawlist(self):
        for o in self.gamelist:
            gfx.dirty(gfx.surface.blit(*o))

    def moveship(self):
        pos = list(self.shipimage[1].topright)
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

        self.shipimage[1].topright = pos


    def pressed(self):
        pref = Options[self.current]
        snd.play('select_choose')
        val = Options[self.current].split()[0].lower()
        getattr(self, "do_"+val)()


    def do_main(self): #Main Menu
        self.quit()

    def do_download(self): #Download News
        self.download_start()

    def do_visit(self): #Visit Website
        if game.display: #fullscreen
            self.tempwindowed = 1
            game.display = 0
            gfx.switchfullscreen()
        self.launchthebrowser = 2 #funny windows workaround

