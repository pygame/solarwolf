"""graphics class, helps everyone to draw"""

import pygame, pygame.image
from pygame.locals import *

import game, stars

#the accessable screen surface and size
surface = None
rect = Rect(0, 0, 0, 0)

#the accessable dirty rectangles
dirtyrects = []


starobj = None


def initialize(size, fullscreen):
    global surface, rect, starobj
    try:
        flags = 0
        if fullscreen:
            flags |= FULLSCREEN
        depth = pygame.display.mode_ok(size, flags, 16)
        surface = pygame.display.set_mode(size, flags, depth)
        rect = surface.get_rect()

        pygame.mouse.set_visible(0)
        
        if surface.get_bytesize() == 1:
            loadpalette()
            
    except pygame.error, msg:
        import messagebox
        messagebox.error('Cannot Initialize Graphics', msg.args[0])
    starobj = stars.Stars()


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
    dirtyrects = []


def text(font, color, text, center=None, pos='center'):
    bgd = 0, 0, 0
    if text is None: text = ' '
    try:
        if surface.get_bytesize()>1:
            img = font.render(text, 1, color, bgd)
            img.set_colorkey(bgd, RLEACCEL)
        else:
            img = font.render(text, 0, color)
        img = img.convert()
    except (pygame.error, TypeError):
        #print 'TEXTFAILED', text
        img = pygame.Surface((10, 10))
        #raise
    r = img.get_rect()
    if center: setattr(r, pos, center)
    return [img, r]


def load(name):
    img = load_raw(name)
    #use rle acceleration if no hardware accel
    if not surface.get_flags() & HWSURFACE:
        pass
        clear = img.get_colorkey()
        if clear:
            img.set_colorkey(clear, RLEACCEL)
    return img.convert()


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
