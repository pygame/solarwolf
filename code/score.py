# solarwolf - collecting and dodging arcade game
# Copyright (C) 2006  Pete Shinners <pete@shinners.org>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#score rendering routines

import pygame
from pygame.locals import RLEACCEL
import gfx


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
