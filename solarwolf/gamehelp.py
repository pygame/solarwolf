"""in game help screens"""

import math
import pygame
from pygame.locals import *
import game
import gfx, snd, txt
import input
import gameplay, objtext

fonts = []

def load_game_resources():
    fonts.append(txt.Font('sans', 10, italic=1))  #----------- 폰트 14에서 10로 변경 -----------
    fonts.append(txt.Font('sans', 15, bold=1))    #----------- 폰트 20에서 15로 변경 -----------
    snd.preload('chimein', 'chimeout')


Help = {
"player":"""SolarWolf 도움말
당신은 강력한 SolarWolf 함대를 조종합니다.
-
무기는 없지만, 가장 뛰어난 기동성을 자랑합니다.
방향키나 조이스틱으로 함선을 조작하세요.
(또한 "vi" 키를 사용할 수도 있습니다. 이게 무엇인지 아신다면요.)
-
스페이스바 또는 조이스틱 버튼을 누르고 있어 Hyper Jets를 활용하세요.
-
각 레벨의 모든 Power Cubes를 모아 다음 레벨로 진행하세요.""",

"multibox":"""색상 Power Cubes
일부 Power Cubes는 다른 색상을 가지며, 이는 SolarWolf 함선이 해당 큐브에 여러 번 접촉해야만 수집할 수 있음을 의미합니다.""",

"guardians":"""Guardian 정보
Guardian들은 각 레벨의 Power Cubes를 보호합니다.
레벨이 높아질수록 그들은 더 공격적으로 변합니다.
-
Guardian 근처로 너무 다가가지 마세요. 가까이에서 공격하기를 좋아합니다.""",

"asteroids":"""운석 경고
운석이 나타나기 시작했습니다. 운석은 닿는 모든 것을 파괴합니다.
-
더 깊은 우주로 나아갈수록 더 많은 운석이 등장할 것입니다.""",

"spikes":"""Spike Mine
이 레벨에는 치명적인 Spike Mine이 있습니다.
접촉하면 함선이 파괴됩니다.""",

"secretspikes":"""숨겨진 Spike Mine
센서는 이 레벨 어딘가에 Spike Mine이 있음을 감지했습니다.
조심하세요. 어디든 나타날 수 있습니다.
-
이 레벨에는 하나의 숨겨진 Spike Mine만 있지만,
더 어려운 레벨에서는 여러 Spike Mine이 등장합니다.""",

"powerup":"""파워업
녹색 Power Up이 나타나면 반드시 획득하세요.
특수 능력과 보너스를 제공합니다.
-
더 어려운 레벨에 도달할수록 더 강력한 효과를 가진 파워업이 등장합니다.""",

"skip":"""레벨 스킵 타이머
화면 오른쪽에 큰 빨간색 레벨 스킵 타이머가 보일 것입니다.
타이머가 끝나기 전에 레벨을 클리어하면,
다음 레벨을 자동으로 건너뛸 수 있습니다.""",

"Skip Bonus":"""시간 스킵 파워업
이 파워업은 레벨 스킵 타이머에 더 많은 시간을 추가합니다.
-
이 아이템을 수집하면 레벨을 통과하고
스킵 타이머를 이기기가 훨씬 쉬워집니다.""",

"Shot Blocker":"""샷 차단 파워업
이 파워업은 현재 우주에 있는 모든 탄환을 제거합니다.
상황이 어려울 때 생명을 구해주는 아이템입니다.""",

"Shield":"""방패 파워업
이 파워업은 SolarWolf 함선에 일시적으로 방패를 활성화합니다.
방패가 활성화된 동안 우주를 더 빠르게 비행할 수 있습니다.
-
주의하세요. 방패는 운석으로부터는 보호해주지 않습니다.
-
방패 효과가 사라진 후에도 1초 동안 무적 상태가 유지됩니다.""",

"Bullet Time":"""총알 시간 파워업
이 파워업은 일시적으로 반응 속도를 향상시켜
모든 것이 느리게 움직이는 것처럼 보이게 합니다.
-
몇 초가 지나면 천천히 시간이 빨라지기 시작해
정상 속도로 돌아옵니다.""",

"Extra Life":"""추가 생명 파워업
이 파워업은 SolarWolf 함대에 새로운 함선을 추가합니다.
-
숙련된 플레이와 함께 이 아이템을 사용하면,
기본 함선 3개보다 훨씬 많은 함선을 수집할 수 있습니다.""",

"Combustion":"""Guardian 폭발
이 파워업은 Guardian 중 하나를 폭발시킵니다.
-
폭발된 적은 해당 레벨이 끝날 때까지 사라집니다.""",

"Fast Bullets": """빠른 총알 (디버프)
    이 파워업을 수집하면 모든 총알이 일시적으로 네 배의 속도로 움직입니다.
    -
    빨라지는 총알에 대비하세요!
    -
    이 효과는 정상 속도로 돌아가기 전에 점진적으로 사라집니다.""",

}
#게임 help 메시지 추가


QuickHelp = {
"asteroids":"운석을 조심하세요",
"spikes":"스파이크 지뢰를 조심하세요",
"secretspikes":"숨겨진 스파이크 지뢰를 조심하세요",
"powerup":"파워업을 획득하세요",
"Skip Bonus":"타이머 시간을 추가합니다",
"Shot Blocker":"모든 총알을 제거합니다",
"Shield":"일시적인 무적 상태",
"Bullet Time":"슬로우 모션 효과",
"Extra Life":"추가 생명",
"Combustion":"수호자 하나를 제거합니다",
"Fast Bullets":"총알 속도가 빨라집니다",
}



def help(helpname, helppos):
    if helpname not in game.player.help:
        game.player.help[helpname] = 1
        if game.help == 0:
            game.handler = GameHelp(game.handler, helpname, helppos)
        elif hasattr(game.handler, "textobjs"):
            t = getattr(game.handler, "textobjs")
            message = QuickHelp.get(helpname, None)
            if message and game.comments >= 1:
                t.append(objtext.Text(message))



class GameHelp:
    def __init__(self, prevhandler, helpname, helppos):
        self.prevhandler = prevhandler
        self.helpname = helpname
        self.helppos = helppos
        self.time = 0.0
        self.img = None
        self.rect = None
        self.needdraw = 1
        self.done = 0
        if snd.music:
            vol = snd.music.get_volume()
            if vol:
                snd.music.set_volume(vol * 0.6)
        snd.play('chimein')

        if hasattr(game.handler, 'player'):
            game.handler.player.cmd_turbo(0)

    def quit(self):
        snd.play('chimeout')
        if snd.music:
            snd.tweakmusicvolume()
        if self.rect:
            r = self.rect.inflate(2, 2)
            r = self.prevhandler.background(r)
            gfx.dirty(r)
        game.handler = self.prevhandler
        self.done = 1

    def input(self, i):
        if self.time > 30.0:
            self.quit()

    def event(self, e):
        pass


    def drawhelp(self, name, pos):
        if name in Help:
            text = Help[name]
            lines = text.splitlines()
            for x in range(1, len(lines)):
                if lines[x] == '-':
                    lines[x] = "\n\n"
            title = lines[0]
            text = ' '.join(lines[1:])
        else:
            title = name
            text = "no help available"

        self.img = fonts[0].textbox((255, 240, 200), text, 260, (50, 100, 50), 30)
        r = self.img.get_rect()
        titleimg, titlepos = fonts[1].text((255, 240, 200), title, (r.width/2, 10))
        self.img.blit(titleimg, titlepos)
        r.topleft = pos
        r = r.clamp(game.arena)
        alphaimg = pygame.Surface(self.img.get_size())
        alphaimg.fill((50, 100, 50))
        alphaimg.set_alpha(192)
        gfx.surface.blit(alphaimg, r)
        self.img.set_colorkey((50, 100, 50))
        self.rect = gfx.surface.blit(self.img, r)
        gfx.dirty(self.rect)


    def run(self):
        if self.needdraw:
            self.needdraw = 0
            self.drawhelp(self.helpname, self.helppos)

        ratio = game.clockticks // 25
        speedadjust = max(ratio, 1.0)
        self.time += speedadjust

        if not self.done:
            pts = (self.rect.topleft, self.rect.topright,
                  self.rect.bottomright, self.rect.bottomleft)
            s = gfx.surface
            clr = 40, 80, 40
            gfx.dirty(pygame.draw.line(s, clr, pts[0], pts[1]))
            gfx.dirty(pygame.draw.line(s, clr, pts[1], pts[2]))
            gfx.dirty(pygame.draw.line(s, clr, pts[2], pts[3]))
            gfx.dirty(pygame.draw.line(s, clr, pts[3], pts[0]))
            off = int(self.time * 0.9)
            r = 255
            g = int(220 + math.cos(self.time * .2) * 30)
            b = int(180 + math.cos(self.time * .2) * 65)
            clr = r, g, b
            gfx.drawvertdashline(s, pts[0], pts[3], clr, 10, off)
            gfx.drawvertdashline(s, pts[1], pts[2], clr, 10, -off)
            gfx.drawhorzdashline(s, pts[0], pts[1], clr, 10, off)
            gfx.drawhorzdashline(s, pts[3], pts[2], clr, 10, -off)

        #gfx.updatestars(self.background, gfx)


    def background(self, area):
        return gfx.surface.fill((0, 0, 0), area)



