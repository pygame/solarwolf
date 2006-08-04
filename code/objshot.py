#simple enemy class

import pygame, pygame.image
from pygame.locals import *
import gfx, game, random, math

rng = random.Random()

images = []
allimages = []
darkimages = []

#glowstuff adjusted from updateglow func
glowtime = 0.0
glowset = 0

def load_game_resources():
    #load shot graphics
    global images, allimages, darkimages
    img = gfx.load_raw('fire.png')
    origpal = img.get_palette()
    img.set_colorkey(img.get_at((0,0)))
    images = gfx.animstrip(img)
    allimages.append(images)

    for x in range(10, 181, 10):
        pal = [(max(r-x*.28,0), max(g-x*.48,0), min(b+x*.38,255))
                for (r,g,b) in origpal]
        img.set_palette(pal)
        allimages.append(gfx.animstrip(img))

    for i in gfx.animstrip(img):
        i.set_alpha(128, RLEACCEL)
        darkimages.append(i)


def updateglow(speedadjust):
    global glowtime, glowset, allimages
    glowtime += speedadjust * .2
    glowset = int((math.sin(glowtime)*.5+.5) * len(allimages))


class Shot:
    blockrocks = 1
    def __init__(self, pos, move):
        self.move = move
        self.images = images
        self.numframes = len(self.images)
        self.frame = random.random() * 3.0
        self.rect = self.images[0].get_rect()
        self.rect.center = pos
        self.darkrect = Rect(self.rect)
        self.lastrect = None
        self.dead = 0
        self.pos = list(self.rect.topleft)
        self.time = 0.0
        self.numbrights = float(len(images))

    def prep(self, screen):
        pass

    def erase(self, background):
        if self.lastrect:
            background(self.lastrect)
            if self.dead:
                gfx.dirty(self.lastrect)
                self.lastrect = None

    def draw(self, gfx):
        frame = int(self.frame-1.0) % self.numframes
        img = darkimages[frame]
        r2 = gfx.surface.blit(img, self.rect.move(-self.move[0]*2, -self.move[1]*2))

        frame = int(self.frame) % self.numframes
        img = allimages[glowset][frame]
        r1 = gfx.surface.blit(img, self.rect)

        #gfx.dirty2(r, self.lastrect)
        r = r1.union(r2)
        gfx.dirty2(r, self.lastrect)
        self.lastrect = r

    def tick(self, speedadjust = 1.0):
        self.frame += speedadjust * .5
        self.pos[0] += self.move[0] * speedadjust
        self.pos[1] += self.move[1] * speedadjust
        self.time += speedadjust * .1
        self.images = images[int(math.cos(self.time)*self.numbrights)]
        self.rect.topleft = self.pos
        if not gfx.rect.colliderect(self.rect):
            self.dead = 1
        return self.dead


#manage fire glitter
#beware unused, looks mediorce, runs slow
class Glitter:
    def __init__(self):
        self.dots = []

    def update(self, speedadjust):
        black = gfx.surface.map_rgb(0, 0, 0)
        draw = gfx.surface.fill
        dirty = gfx.dirtyrects.append
        oneone = 1, 1

        dead = 0
        prelen = len(self.dots)
        for dot in self.dots:
            if not dot[1]:
                break
            dead += 1
        if dead > 50:
            del self.dots[:dead]

        driftCount = 0
        for i in range(len(self.dots)-1, -1, -1):
            driftCount = (driftCount+1) % 6

            dot = self.dots[i]
           #dot[0] is intensity
           #dot[1] is ( color, rect )
           #dot[2] is the originating ball's center
            if dot[0] > 12.0:
                if dot[1]:
                    dirty(draw(black, dot[1][1]))
                    dot[1] = 0
            else:
                if driftCount == 1:
                    dirty( draw(black, dot[1][1]) )
                    dot[1][1].x = rng.randint( dot[2][0] - 2, dot[2][0] + 3)
                    dot[1][1].y = rng.randint( dot[2][1] - 2, dot[2][1] + 3)
                draw(*dot[1])
                dot[0] += speedadjust



    def add(self, balls, ratio):
        amount = ratio * 4.0
        map = gfx.surface.map_rgb
        _min = min
        _max = max
        _int = int
        rnd = random.random
        append = self.dots.append
        draw = gfx.surface.fill
        dirty = gfx.dirtyrects.append
        for b in balls:
            if b.dead:
                continue
            x, y = b.rect.center
            for d in range( _max( 0, rng.randrange( amount-2, amount+3 ) ) ):
                lived = rnd()
                r = _min(255, _int(100.0+lived*100.0))
                g = _min(255, _int( 20.0+lived*240.0))
                b = _min(255, _int( 2.0+lived*30.0))
                color = map(r, g, b)
                r1 = rng.randrange( -5, 6 )
                r2 = rng.randrange( -5, 6 )
                #r1 = abs(r1*r1*(3-r1-r1)-.5)*10.0
                #r2 = abs(r2*r2*(3-r2-r2)-.5)*10.0
                size = rng.randrange( 1, 3 )
                r = Rect(r1 + x, r2 + y, size, size)
                append( [lived * 9.0, (color, r), (x,y)] )
                draw(color, r)
