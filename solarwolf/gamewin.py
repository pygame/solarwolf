"gamemenu handler. main menu"

import math, os
import pygame
from pygame.locals import *
import game, gfx, snd, txt
import gameplay, gamemenu, players


#--- 한글로 변경 ---
cheer_korean = (
    '축하합니다!',
    '당신은 게임을 클리어했습니다!',
    ' ',
    '알려진 은하는 다시 한 번 안전해졌습니다.',
    '모두의 시야를 가로막던 보기 흉한 파워 큐브들로부터 말이죠.',
    '치명적인 가디언의 어지러운 계획은',
    '당신의 기지와 기술로 좌절되었습니다.',
    '',
    '우리는 이 위협이 다시는 돌아오지 않기를 바랍니다.',
    '그러나 필요하다면 SolarWolf의 힘이',
    '다시 한 번 시험대에 오를 것입니다.',
)


fonts = []

def load_game_resources():
    global fonts
    fontname = None
    fonts.append(txt.Font(fontname, 28))
    snd.preload('select_choose')


class GameWin:
    def __init__(self, prevhandler):
        self.prevhandler = prevhandler
        self.done = 0
        self.top = 20
        self.center = gfx.rect.centerx
        self.text = []
        self.time = 0.0
        font = fonts[0]
        for line in cheer:
            img, r = font.text((250, 250, 250), line, (self.center, self.top))
            self.top += 30
            self.text.append((img, r))
        self.g = gamemenu.boximages
        self.y = gamemenu.yboximages
        self.r = gamemenu.rboximages



    def quit(self):
        if not game.player:
            game.player = players.Player("NONAME")
        players.make_winner(game.player)

        game.handler = self.prevhandler
        self.done = 1
        snd.play('select_choose')

        r = self.r[0].get_rect()
        gfx.dirty(self.background(r.move(50, 400)))
        gfx.dirty(self.background(r.move(300, 400)))
        gfx.dirty(self.background(r.move(550, 400)))


    def input(self, i):
        if self.time > 30.0:
            self.quit()

    def event(self, e):
        pass


    def run(self):
        for cred in self.text:
            r = cred[1]
            self.background(r)
            gfx.dirty(r)

        ratio = game.clockticks // 25
        speedadjust = max(ratio, 1.0)
        self.time += speedadjust

        gfx.updatestars(self.background, gfx)

        if not self.done:
            frame = int(self.time * .5) % len(self.r)
            surf = gfx.surface
            gfx.dirty(surf.blit(self.g[frame], (50, 400)))
            gfx.dirty(surf.blit(self.y[frame], (300, 400)))
            gfx.dirty(surf.blit(self.r[frame], (550, 400)))

            for cred, pos in self.text:
                gfx.surface.blit(cred, pos)


    def background(self, area):
        return gfx.surface.fill((0, 0, 0), area)



