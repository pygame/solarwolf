#score rendering routines

import pygame
from pygame.locals import *
import game, gfx, math
from random import randint


img_1 = None
img_5 = None
img_10 = None
img_50 = None


def load_game_resources():
    global img_1, img_5, img_10, img_50
    img_1 = gfx.load('score_1.png')
    img_5 = gfx.load('score_5.png')
    img_10 = gfx.load('score_10.png')
    img_50 = gfx.load('score_50.png')


def render(score):
    imgs = []

    if score <= 0:
        out = pygame.Surface(img_1.get_size()).convert()
        out.set_colorkey(0, RLEACCEL)
        return out
    
    if score >= 50:
        imgs.append(img_50)
        score -= 50
    while score >= 40:
        imgs.append(img_10)
        imgs.append(img_50)
        score -= 40
    while score >= 10:
        imgs.append(img_10)
        score -= 10
    while score >= 9:
        imgs.append(img_1)
        imgs.append(img_10)
        score -= 9
    while score >= 5:
        imgs.append(img_5)
        score -= 5
    while score >= 4:
        imgs.append(img_1)
        imgs.append(img_5)
        score -= 4
    while score:
        imgs.append(img_1)
        score -= 1

    width = 0
    for i in imgs:
        width += i.get_width()
    
    out = pygame.Surface((width, img_1.get_height())).convert()
    pos = 0
    for i in imgs:
        out.blit(i, (pos, 0))
        pos += i.get_width()

    out.set_colorkey(0, RLEACCEL)
    return out
