#powerup class

import random
import pygame
from pygame.locals import *
import game, gfx, snd, objpopshot


images = []

def load_game_resources():
    global images
    for letter in 'bcdef':
        img = gfx.load('powerup_' + letter + '.png')
        images.append(img)
    snd.preload('select_choose')


class Powerup:
    def __init__(self):
        self.images = images
        self.image = self.images[0]
        self.speed = game.powerupspeed
        r = random.randint(0, 1200)
        if r < 700:
            self.pos = [float(r), 0.0]
        else:
            self.pos = [0.0, float(r - 700)]
        self.rect = self.image.get_rect()
        self.rect.move_ip(-20, -20)
        self.time = 0
        self.dead = 0

    def erase(self, background):
        r = background(self.rect)
        #if self.dead:
        gfx.dirty(r)

    def draw(self, gfx):
        img = self.image
        r = gfx.surface.blit(img, self.rect)
        gfx.dirty(r)

    def tick(self, speedadjust):
        self.pos[0] = (self.pos[0] + speedadjust*self.speed) % 740
        self.pos[1] = (self.pos[1] + speedadjust*self.speed) % 640
        self.rect.topleft = self.pos
        self.rect.move_ip(-20, -20)
        self.time += speedadjust
        frame = int((self.time * .3)) % len(self.images)
        self.image = self.images[frame]
        if self.time >= game.poweruptime:
            self.dead = 1

    def extendtime(self):
        self.time -= 20.0


class PowerupEffect:
    "Generic Powerup"
    runtime = 100.0
    def __init__(self):
        self.time = 0.0
        self.state = game.handler
        self.dead = 0
        self.start()

    def tick(self, speedadjust):
        self.time += speedadjust
        if self.time >= self.runtime:
            self.dead = 1
        pass

    def start(self):
        pass

    def end(self):
        pass


class ExtraLevelTime(PowerupEffect):
    "Skip Bonus"
    runtime = 200.0
    def start(self):
        snd.play('levelskip')
        self.origtick = game.timetick
        game.timetick = game.timetick / -2
        #for s in self.state.asteroidobjs[:2]:
        #    s.dead = 1
        #    self.state.popobjs.append(objpopshot.PopShot(s.rect.center))

    def end(self):
        game.timetick = self.origtick

class Shield(PowerupEffect):
    "Shield"
    runtime = 200.0
    def start(self):
        snd.play('select_choose')
        self.state.player.shield += 2
        self.ending = 0

    def tick(self, speedadjust):
        PowerupEffect.tick(self, speedadjust)
        if not self.ending and self.time >= 170.0:
            self.ending = 1
            self.state.player.shield -= 1

    def end(self):
        if self.ending:
            self.state.player.shield -= 1
        else:
            self.state.player.shield -= 2

class PopShots(PowerupEffect):
    "Shot Blocker"
    runtime = 1.0
    def start(self):
        snd.play('whip')
        for s in self.state.shotobjs:
            s.dead = 1
            self.state.popobjs.append(objpopshot.PopShot(s.rect.center))
        #for s in self.state.asteroidobjs[:2]:
        #    s.dead = 1
        #    self.state.popobjs.append(objpopshot.PopShot(s.rect.center))

class ExtraLife(PowerupEffect):
    "Extra Life"
    runtime = 1.0
    def start(self):
        snd.play('delete')
        self.state.lives_left += 1
        self.state.hud.drawlives(self.state.lives_left)

class SlowMotion(PowerupEffect):
    "Bullet Time"
    runtime = 140.0
    def start(self):
        snd.play('gameover')
        game.speedmult += 2
        self.ending = 0

    def tick(self, speedadjust):
        PowerupEffect.tick(self, speedadjust)
        if not self.ending and self.time >= 120.0:
            self.ending = 1
            game.speedmult -= 1

    def end(self):
        if self.ending:
            game.speedmult -= 1
        else:
            game.speedmult -= 2

effects = ExtraLevelTime, PopShots, Shield, SlowMotion, ExtraLife
