"""graphics class, helps everyone to draw"""

import sys, platform, pygame, pygame.image
from pygame.locals import *

import game, stars

IS_MAC = 'Darwin' in platform.system()

#the accessable screen surface and size
surface = None
rect = Rect(0, 0, 0, 0)

#the accessable dirty rectangles
dirtyrects = []


starobj = None
wantscreentoggle = 0


def initialize(size, fullscreen):
    global surface, rect, starobj
    try:
        flags = 0
        if fullscreen:
            flags |= FULLSCREEN
        #depth = pygame.display.mode_ok(size, flags, 16)
        surface = pygame.display.set_mode(size, flags)#, depth)
        rect = surface.get_rect()

        pygame.mouse.set_visible(0)

        if surface.get_bytesize() == 1:
            loadpalette()

    except pygame.error as msg:
        raise pygame.error('Cannot Initialize Graphics')
    starobj = stars.Stars()


def switchfullscreen():
    oldfull = surface.get_flags() & FULLSCREEN == FULLSCREEN
    newfull = game.display == 1
    if newfull == oldfull:
        return
    global wantscreentoggle
    wantscreentoggle = 1



def dirty(rect):
    dirtyrects.append(rect)


def dirty2(rect1, rect2):
    if not rect2:
        dirtyrects.append(rect1)
    elif rect.colliderect(rect2):
        dirtyrects.append(rect1.union(rect2))
    else:
        dirtyrects.append(rect1)
        dirtyrects.append(rect2)


def updatestars(bgd, gfx):
    starobj.erase_tick_draw(bgd, gfx)


def update():
    global dirtyrects
    pygame.display.update(dirtyrects)
    #dirtyrects = []
    del dirtyrects[:]

    global wantscreentoggle
    if wantscreentoggle:
        wantscreentoggle = 0
        if game.handler:
            starobj.eraseall(game.handler.background, sys.modules[__name__])
        screencapture = pygame.Surface(surface.get_size())
        screencapture.blit(surface, (0,0))
        clipcapture = surface.get_clip()
        initialize(surface.get_size(), game.display)
#        if game.handler:
#            game.handler.background(rect)
        surface.blit(screencapture, (0,0))

        pygame.display.update()
        surface.set_clip(clipcapture)


def optimize(img):
    #~ if surface.get_alpha():
        #~ img.set_alpha()
        #~ if surface.get_flags() & HWSURFACE:
            #~ img.set_colorkey(0)
        #~ else:
            #~ img.set_colorkey(0, RLEACCEL)
    #~ elif not surface.get_flags() & HWSURFACE:

    if IS_MAC:
        # SDL2 MacOS fix. See https://github.com/pygame/pygame/issues/721
        if not surface.get_flags() & HWSURFACE:
            clear = img.get_colorkey()
            if clear:
                img.set_colorkey(clear, RLEACCEL)
                return img.convert()
        return img.convert_alpha()

    if not surface.get_flags() & HWSURFACE:
        clear = img.get_colorkey()
        if clear:
            img.set_colorkey(clear, RLEACCEL)
    return img.convert()

def load(name):
    img = load_raw(name)
    #use rle acceleration if no hardware accel
    return optimize(img)

def load_raw(name):
    file = game.get_resource(name)
    img = pygame.image.load(file)
    return img


def loadpalette():
    file = open(game.get_resource('solarwolf.pal'))
    pal = []
    for line in file.readlines()[3:]:
        vals = [int(x) for x in line.split()]
        pal.append(vals)
    surface.set_palette(pal)



#thanks to MU
def drawvertdashline(dstsurf, startpos, endpos, color, dashsize, offset):
    """drawvertdashline

    dstsurf = surface on which line is drawn
    startpos, endpos = (x0, y0), (x0, y1) of line
    color = RGB(A) of line; between dashes is nothing
    dashsize = pixel length of on, and of off sections
    offset = where to start"""

    x, y0 = startpos
    x, y1 = endpos

    if y1 < y0:
        y0, y1 = y1, y0

    period = 2*dashsize
    offset = offset % period
    starts = [ max(y,y0)
        for y in range(y0-period+offset, y1+period, 2*dashsize)
        if y0-dashsize < y < y1 ]
    stops = [ min(y-1,y1)
        for y in range(y0-dashsize+offset, y1+period, 2*dashsize)
        if y0 < y < y1+dashsize ]

    for b,e in zip(starts, stops):
        #pygame.draw.line(dstsurf, color, (x,b), (x,e))
        dstsurf.fill(color, (x,b,1,e-b+1))

def drawhorzdashline(dstsurf, startpos, endpos, color, dashsize, offset):
    """drawhorzdashline

    dstsurf = surface on which line is drawn
    startpos, endpos = (x0, y0), (x0, y1) of line
    color = RGB(A) of line; between dashes is nothing
    dashsize = pixel length of on, and of off sections
    offset = where to start"""

    x0, y = startpos
    x1, y = endpos

    if x1 < x0:
        x0, x1 = x1, x0

    period = 2*dashsize
    offset = offset % period
    starts = [ max(x,x0)
        for x in range(x0-period+offset, x1+period, 2*dashsize)
        if x0-dashsize < x < x1 ]
    stops = [ min(x-1,x1)
        for x in range(x0-dashsize+offset, x1+period, 2*dashsize)
        if x0 < x < x1+dashsize ]

    for b,e in zip(starts, stops):
        #pygame.draw.line(dstsurf, color, (x,b), (x,e))
        dstsurf.fill(color, (b,y,e-b+1,1))



def animstrip(img, width=0):
    if not width:
        width = img.get_height()
    size = width, img.get_height()
    images = []
    origalpha = img.get_alpha()
    origckey = img.get_colorkey()
    img.set_colorkey(None)
    img.set_alpha(None)
    for x in range(0, img.get_width(), width):
        i = pygame.Surface(size)
        i.blit(img, (0, 0), ((x, 0), size))
        if origalpha:
            i.set_colorkey((0,0,0))
        elif origckey:
            i.set_colorkey(origckey)
        images.append(optimize(i))
    img.set_alpha(origalpha)
    img.set_colorkey(origckey)
    return images
