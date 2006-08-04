"gameplay handler. for the main part of the game"

import pygame
from pygame.locals import *
import random, math

import game, gfx, input, snd
import gamehelp, gamepause
import objship, objbox, objguard, objshot, objexplode, objtele
import objpopbox, objpopshot, objtext, objsmoke, objwarp
import objpowerup, objasteroid
import levels, hud, players

#num of insults must match num of complements
Complements = (
    'Keep it up!',
    'Looking Great!',
    'Hotshot',
    'Too Hot to Handle',
    'Lord of the Dance',
    'Bring it on',
    'Beautiful',
    'Own the Zone',
    'Too Cool For School',
    'So Hot Right Now',
    'Smooth Moves'
)
Insults = (
    'Not so good',
    'Ouch',
    'Look away',
    'Rookie',
    'Sloppy',
    'Choke Choke',
    'Not Today',
    'Hall of Shame',
    'Wrong way',
    'Clumsy, Clumsy',
    'Medic',
)


def load_game_resources():
    snd.preload('gameover', 'startlife', 'levelskip', 'explode')
    snd.preload('boxhot', 'levelfinish', 'shoot', 'whip')


class GamePlay:
    def __init__(self, prevhandler):
        self.startlevel = game.player.start_level()
        self.newcontinue = 0
        self.levelnum = -1
        self.gamewon = 0
        self.player = objship.Ship()
        self.prevhandler = prevhandler
        self.staticobjs = []
        self.boxobjs = []
        self.shotobjs = []
        self.powerupobjs = []
        self.powereffects = []
        self.popobjs = []
        self.textobjs = []
        self.smokeobjs = []
        self.asteroidobjs = []
        self.guardobjs = [objguard.Guard(x) for x in range(4)]
        self.objlists = [self.boxobjs, self.shotobjs, self.popobjs, self.smokeobjs,
                         self.powerupobjs, self.asteroidobjs, self.guardobjs,
                         self.staticobjs, self.textobjs]
        self.hud = hud.HUD()

        self.state = ''
        self.statetick = self.dummyfunc
        self.lives_left = 0
        self.grabbedboxes = 0
        self.powerupcount = 0.0
        self.numdeaths = 0
        self.complement = random.randint(0, len(Complements)-1)

        self.lasttick = pygame.time.get_ticks()
        self.speedadjust = 1.0
        self.startmusic = 1

        self.changestate('gamestart')

        self.bgfill = gfx.surface.fill



    def starting(self):
        if self.startmusic:
            self.startmusic = 0
            snd.playmusic('arg.xm')

    def gamewin(self):
        self.gamewon = 1
        self.changestate('gameover')
        self.textobjs.append(objtext.Text('GAME WINNER!'))

    def changestate(self, state):
        getattr(self, self.state+'_end', self.dummyfunc)()
        self.state = state
        getattr(self, state+'_start', self.dummyfunc)()
        self.statetick = getattr(self, state+'_tick')

    def dummyfunc(self): pass

    def userquit(self):
        if self.state == 'gameover': return
        if self.lives_left and self.player.active:
            self.lives_left = 0
            self.changestate('playerdie')
        else:
            self.changestate('gameover')

    def input(self, i):
        if i.release:
            if i.translated == input.PRESS:
                self.player.cmd_turbo(0)
        else:
            if i.translated == input.ABORT:
                self.userquit()
            elif i.translated == input.UP:
                self.player.cmd_up()
            elif i.translated == input.DOWN:
                self.player.cmd_down()
            elif i.translated == input.LEFT:
                self.player.cmd_left()
            elif i.translated == input.RIGHT:
                self.player.cmd_right()
            elif i.translated == input.PRESS:
                self.player.cmd_turbo(1)


    def event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_PAUSE or e.key == pygame.K_p:
                game.handler = gamepause.GamePause(self)

    def run(self):
        ratio = game.clockticks / 25
        self.speedadjust = max(ratio, 1.0)
        if game.speedmult >= 2:
            self.speedadjust *= 0.35
        elif game.speedmult: #if true must be 1
            self.speedadjust *= 0.55
        self.statetick()


    def runobjects(self, objects):
        G, B, S = gfx, self.background, self.speedadjust
        gfx.updatestars(B, G)
        for effect in self.powereffects[:]:
            if effect.dead:
                effect.end()
                self.powereffects.remove(effect)
            else:
                effect.tick(S)

        #add pop for timedout powerups, sad place to do this, but owell
        for o in self.powerupobjs:
            if o.dead:
                self.popobjs.append(objpopbox.PopBox(o.rect.center))

        for l in objects:
            for o in l[:]:
                o.erase(B)
                o.tick(S)
                if o.dead:
                    o.erase(B)
                    l.remove(o)
        for l in objects:
            for o in l:
                o.draw(G)
        self.hud.draw()

    def background(self, area):
        return self.bgfill(0, area)

    def tickleveltime(self, speedadjust=1):
        if game.timeleft or game.timetick<0:
            game.timeleft = game.timeleft - game.timetick * speedadjust
            if game.timeleft < 0:
                game.timeleft = 0.0



#normal play
    def normal_start(self):
        self.clocks = 0
        if self.levelnum == 0:
            gamehelp.help("player", (250, 100))
        elif self.levelnum == 1:
            gamehelp.help("guardians", (20, 700))
        elif self.levelnum == 2:
            gamehelp.help("skip", (700, 400))
        elif self.levelnum == 3:
            gamehelp.help("multibox", (220, 220))

        if len(self.asteroidobjs):
            gamehelp.help("asteroids", self.asteroidobjs[0].rect.center)


    def normal_tick(self):
        #assert(self.player.active)

        #fire the guards
        shootchance = game.guard_fire * self.speedadjust
        if self.player.active and random.random() < shootchance:
            self.powerupcount += 0.3
            baddy = self.guardobjs[random.randint(0,3)]
            if not baddy.reloading:
                baddy.reloading = objguard.guard_loadtime
            else:
                baddy.waitshots += 1
        for baddy in self.guardobjs:
            if baddy.waitshots and not baddy.reloading:
                baddy.fireme = 0
                baddy.reloading = objguard.guard_loadtime/3
                baddy.waitshots -= 1
            if not baddy.fireme: continue
            shotspot, shotdir = baddy.shotinfo()
            s = objshot.Shot(shotspot, shotdir)
            self.shotobjs.append(s)
            snd.play('shoot', 1.0, shotspot[0])

        #add a powerup if ready
        if self.powerupcount >= 46.0:
            self.powerupcount = 0.0
            p = objpowerup.Powerup()
            self.powerupobjs.append(p)
            snd.play('startlife', 0.3)
            gamehelp.help("powerup", p.rect.topleft)
        if self.grabbedboxes >= 50:
            self.grabbedboxes = 0
            self.textobjs.append(objtext.Text(Complements[self.complement]))
            self.complement = (self.complement + 1) % len(Complements)
        elif self.grabbedboxes >= 20:
            self.numdeaths = 0

        self.tickleveltime(self.speedadjust)

        playerrect = self.player.rect.inflate(-1, -1)
        playercollide = playerrect.colliderect
        #collide player to boxes
        for b in self.boxobjs:
            status = b.playercollide(playerrect)
            if status:
                self.grabbedboxes += 1
                self.powerupcount += 0.6
                if status == 1:
                    self.powerupcount += 0.3
                    b.dead = 1
                    self.popobjs.append(objpopbox.PopBox(b.rect.center))
        #collide player to powerups
        for p in self.powerupobjs:
            if playercollide(p.rect):
                p.dead = 1
                choices = objpowerup.effects[:2+(self.levelnum/8)]
                effect = random.choice(choices)()
                self.textobjs.append(objtext.Text('"'+effect.__doc__+'"'))
                self.powereffects.append(effect)
                gamehelp.help(effect.__doc__, self.player.rect.center)
        playerrect = playerrect.inflate(-6, -6)
        playercollide = playerrect.colliderect
        asteroidrects = [o.colliderect for o in self.asteroidobjs]
        hitbullet = 0
        #collide player and asteroids to bullets
        for s in self.shotobjs:
            r = s.rect
            if playercollide(r):
                s.dead = 1
                if not self.player.shield:
                    self.changestate('playerdie')
                    hitbullet = 1
                else:
                    self.popobjs.append(objpopshot.PopShot(s.rect.center))
            for ar in asteroidrects:
                if ar.colliderect(r) and not s.dead:
                    s.dead = 1
                    self.popobjs.append(objpopshot.PopShot(s.rect.center))
                    break
        #collide player to asteroids
        if not hitbullet:
            for a,r in zip(self.asteroidobjs, asteroidrects):
                if playercollide(r):
                    self.changestate('playerdie')
                    a.dead = 1
                    self.popobjs.append(objpopshot.PopShot(r.center))

        if not self.boxobjs:
            self.changestate('levelend')

        #blow smoke (turbo)
        self.clocks += 1
        if self.player.turbo and (self.player.move[0] or self.player.move[1]) and gfx.surface.get_bytesize()>1:
            self.smokeobjs.append(objsmoke.Smoke(self.player.rect.center))
            if game.clock.get_fps() > 35.0:
                self.smokeobjs.append(objsmoke.Smoke(self.player.rect.center))

        self.runobjects(self.objlists)



#player die
    def playerdie_start(self):
        snd.play('explode', 1.0, self.player.rect.centerx)
        self.explode = objexplode.Explode(self.player.rect.center)
        self.staticobjs.append(self.explode)
        self.poptime = 3
        self.player.dead = 1
        self.player.active = 0
        self.grabbedboxes = 0
        self.numdeaths += 1
        if len(self.boxobjs) <= 2:
            self.textobjs.append(objtext.Text('Doh, so close'))
        elif self.numdeaths > 1:
            self.textobjs.append(objtext.Text(Insults[self.complement]))
            self.complement = (self.complement + 1) % len(Insults)
        for effect in self.powereffects:
            effect.dead = 1


    def playerdie_tick(self):
        self.poptime -= 1
        if not self.poptime:
            self.poptime = 2
            if self.shotobjs:
                s = self.shotobjs[0]
                s.dead = 1
                self.popobjs.append(objpopshot.PopShot(s.rect.center))
        if self.explode.dead and not self.popobjs :#and not game.timeleft:
            if self.lives_left:
                self.lives_left -= 1
                self.hud.drawlives(self.lives_left)
                self.changestate('playerstart')
                if not self.lives_left:
                    self.textobjs.append(objtext.Text("Last Ship, Don't Blow It"))
            else:
                self.changestate('gameover')
        self.tickleveltime(self.speedadjust)
        self.runobjects(self.objlists)

    def playerdie_end(self):
        del self.explode
        del self.poptime



#player start
    def playerstart_start(self):
        snd.play('startlife', 1.0, self.startpos[0])
        self.hud.drawlives(self.lives_left)
        self.powerupcount = max(0.0, self.powerupcount - 15.0)
        self.teleport = objtele.Tele(self.startpos)
        self.popobjs.append(self.teleport)
        self.grabbedboxes = 0

    def playerstart_tick(self):
        #when animations done
        anyblock = 0
        collide = self.teleport.rect.inflate(10, 10).colliderect
        for a in self.asteroidobjs:
            if collide(a.rect) or collide(a.predictrect()):
                anyblock = 1
                break
        if not anyblock:
            self.teleport.rocksclear = 1
        if self.teleport.dead:
            self.changestate('normal')
            self.player.start(self.startpos)
            self.staticobjs.append(self.player)
        self.runobjects(self.objlists)
        #self.tickleveltime(self.speedadjust)

    def playerstart_end(self):
        input.resetexclusive()
        input.postactive()
        del self.teleport


#level start
    def levelstart_start(self):
        self.skipping = game.timeleft > 0.0
        self.levelnum += 1
        del self.boxobjs[:]
        self.newboxes, self.startpos, msg, num = levels.makelevel(self.levelnum)
        self.calcboxes = num
        self.addtime = 2
        if game.clock.get_fps() < 25:
            self.addtime = 1
        self.hud.drawlevel(self.levelnum)
        self.textobjs.append(objtext.Text(msg)) #MSG
        self.grabbedboxes = 0
        self.numdeaths = 0

        if self.levelnum > game.player.score:
            game.player.score = self.levelnum
        if not self.newcontinue and game.player.start_level() > self.startlevel:
            self.newcontinue = 1

        for i in range(levels.numrocks(self.levelnum) - len(self.asteroidobjs)):
            self.asteroidobjs.append(objasteroid.Asteroid())

        for p in self.powerupobjs:
            p.extendtime()

        if self.skipping: self.skiptime = 20


    def levelstart_tick(self):
        self.addtime -= 1
        if not self.addtime:
            self.addtime = 2
            if self.newboxes:
                b = random.choice(self.newboxes)
                self.boxobjs.append(b)
                self.newboxes.remove(b)
        if game.timeleft < 1000.0 and not self.skipping:
            game.timeleft = min(game.timeleft + 25.0, 1000.0)
        if self.skipping:
            if not self.newboxes:
                self.skiptime -= 1
                if not self.skiptime:
                    self.changestate('levelskip')
        else:
            if game.timeleft == 1000.0 and not self.newboxes:
                self.changestate('playerstart')
        self.runobjects(self.objlists)

    def levelstart_end(self):
        del self.newboxes
        del self.skipping
        pct = 1.0 - (self.levelnum / 50.0)
        pct = 1.0 - (pct * pct)
        game.guard_fire = .01 + pct * game.fire_factor
        if len(self.boxobjs):
            game.timetick = (1000.0 / (self.calcboxes * game.timefactor)) * 0.9
        else:
            game.timetick = 5.0
        if self.levelnum <= 1: game.timetick = 5.05
        del self.calcboxes


#level end
    def levelend_start(self):
        snd.play('levelfinish')
        self.popobjs.append(objwarp.Warp(self.player.rect.center))
        self.player.dead = 1
        self.player.active = 0
        self.poptime = 2
        for effect in self.powereffects:
            effect.dead = 1
        if self.grabbedboxes >= 40:
            self.textobjs.append(objtext.Text(Complements[self.complement]))
            self.complement = (self.complement + 1) % len(Complements)

    def levelend_tick(self):
        self.poptime -= 1
        if not self.poptime:
            self.poptime = 2
            if self.shotobjs:
                s = self.shotobjs[0]
                s.dead = 1
                self.popobjs.append(objpopshot.PopShot(s.rect.center))
        if not self.popobjs and not self.shotobjs and not self.popobjs:
            if self.levelnum+1 >= levels.maxlevels():
                self.gamewin()
            else:
                self.changestate('levelstart')
        self.runobjects(self.objlists)

    def levelend_end(self):
        del self.poptime


#level skip
    def levelskip_start(self):
        snd.play('levelskip')
        self.poptime = 2
        if game.clock.get_fps() < 25:
            self.poptime = 1
        self.textobjs.append(objtext.Text('Level Skipped'))
        self.skiptime = 25

    def levelskip_tick(self):
        if self.skiptime:
            self.skiptime -= 1
        else:
            game.timeleft = max(game.timeleft - 5.0, 0.0)
            self.poptime -= 1
            if not self.poptime:
                self.poptime = 2
                if self.boxobjs:
                    b = random.choice(self.boxobjs)
                    b.dead = 1
                    self.popobjs.append(objpopbox.PopBox(b.rect.center))
            if not game.timeleft and not self.boxobjs and not self.popobjs:
                if self.levelnum+1 >= levels.maxlevels():
                    self.gamewin()
                else:
                    self.changestate('levelstart')
        self.runobjects(self.objlists)

    def levelskip_end(self):
        del self.poptime


#game start
    def gamestart_start(self):
        self.ticks = 0
        self.level = 0
        self.donehud = 0
        sound = snd.fetch('whip')
        self.whip = None
        if sound:
            self.whip = sound.play(-1)


    def gamestart_tick(self):
        self.ticks += 1
        if not self.donehud:
            self.hud.setwidth(self.ticks * 10)
            if self.ticks == 10:
                self.donehud = 1
                self.ticks = 0
        else:
            if not self.ticks % 3 and self.levelnum < self.startlevel-1:
                self.levelnum += 1
                self.hud.drawlevel(self.levelnum)
            if not self.ticks % 16 and self.lives_left < game.start_lives:
                self.lives_left += 1
                self.hud.drawlives(self.lives_left)
            if self.lives_left == game.start_lives and \
                       self.levelnum == self.startlevel-1:
                self.changestate('levelstart')

        self.runobjects([])

    def gamestart_end(self):
        self.textobjs.append(objtext.Text('Begin'))
        if self.whip:
            self.whip.stop()
        del self.ticks
        del self.whip

#game over
    def gameover_start(self):
        snd.play('gameover')
        self.ticks = 5
        if not self.gamewon:
            self.textobjs.append(objtext.Text('Game Over'))

    def gameover_tick(self):
        if game.timeleft:
            game.timeleft = max(game.timeleft - 50, 0)
        else:
            if self.ticks:
                self.ticks -= 1
            self.hud.setwidth(self.ticks * 20)
            if not self.ticks and not self.textobjs:
                for x in self.guardobjs: x.dead = 1
                for x in self.boxobjs: x.dead = 1
                for x in self.popobjs: x.dead = 1
                for x in self.powerupobjs: x.dead = 1
                self.final_game_end()
        self.runobjects(self.objlists)

        B = self.background
        for l in self.objlists:
            for o in l:
                o.erase(B)


    def final_game_end(self):
        nexthandler = self.prevhandler
        if self.gamewon:
            import gamewin
            nexthandler = gamewin.GameWin(nexthandler)
            if not game.player:
                nexthandler = gamename.GameName(nexthandler)
        if self.newcontinue:
            if not game.player in players.players:
                players.players.append(game.player)

            #add a highscore handler into these chains
            if not game.player.name:
                import gamename
                nexthandler = gamename.GameName(nexthandler)

        game.handler = nexthandler



