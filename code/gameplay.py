"gameplay handler. for the main part of the game"

import pygame
from pygame.locals import *
import random

import game, gfx, input, snd
import gamehelp, gamepause
import objship, objbox, objguard, objshot, objexplode, objtele
import objpopshot, objtext, objsmoke, objwarp
import objpowerup, objasteroid
import levels, hud, players


Songs = [('arg.xm', 1.0), ('h2.ogg', 0.6)]

def load_game_resources():
    snd.preload('gameover', 'startlife', 'levelskip', 'explode')
    snd.preload('boxhot', 'levelfinish', 'shoot', 'whip', 'klank2')
    snd.preload('spring', 'flop')


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
        self.spikeobjs = []
        self.powerupobjs = []
        self.powereffects = []
        self.popobjs = []
        self.textobjs = []
        self.smokeobjs = []
        self.asteroidobjs = []
        self.guardobjs = [objguard.Guard(x) for x in range(4)]
        self.objlists = [self.boxobjs, self.shotobjs, self.spikeobjs, self.popobjs,
                         self.smokeobjs, self.powerupobjs, self.asteroidobjs,
                         self.guardobjs, self.staticobjs, self.textobjs]
        self.glitter = objshot.Glitter()
        self.hud = hud.HUD()

        self.state = ''
        self.statetick = self.dummyfunc
        self.lives_left = 0
        self.grabbedboxes = 0
        self.powerupcount = 0.0
        self.numdeaths = 0
        self.secretspikes = []
        self.touchingsecretspike = None
        self.complement = random.randint(0, len(game.Complements)-1)

        self.lasttick = pygame.time.get_ticks()
        self.speedadjust = 1.0
        self.startmusic = 1
        self.song = ''
        self.songtime = 0

        self.changestate('gamestart')

        self.bgfill = gfx.surface.fill


    def starting(self):
        if self.startmusic:
            self.startmusic = 0
            self.song = random.choice(Songs)
            snd.playmusic(*self.song)
            self.songtime = pygame.time.get_ticks()
        gfx.dirty(self.background(gfx.rect))

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
            #What are you doing? Looking for Cheats?
            #shame shame
            if input.Cheatstring == "wheat":
                snd.play('gameover')
                snd.play('delete')
                game.player.cheater = 1
                self.textobjs.append(objtext.Text('"wheat" Cheat: Extra Lives'))
                self.lives_left += 10
                self.hud.drawlives(self.lives_left)
            elif input.Cheatstring == "shred":
                snd.play('gameover')
                snd.play('delete')
                game.player.cheater = 1
                self.grabbedboxes = 0 #less not give any fake complements
                self.levelnum = 49
                self.textobjs.append(objtext.Text('"shred" Cheat: Warp Level 50'))
                self.changestate('levelend')
            if e.key == pygame.K_PAUSE or e.key == pygame.K_p:
                if game.handler is self: #just in case some "help" gets in first?
                    game.handler = gamepause.GamePause(self)

    def run(self):
        if game.handler is not self: #help or pause is taking over
            return
        ratio = game.clockticks / 25
        self.speedadjust = max(ratio, 1.0)
        if game.speedmult >= 2:
            self.speedadjust *= 0.5
        elif game.speedmult: #if true must be 1
            self.speedadjust *= 0.75
        objshot.updateglow(self.speedadjust)
        self.statetick()


    def gotfocus(self):
        pass
    def lostfocus(self):
        if game.handler is self and self.lives_left:
            game.handler = gamepause.GamePause(self)


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
                self.popobjs.append(objpopshot.PopShot(o.rect.center))

        for l in objects:
            for o in l[:]:
                o.erase(B)
                o.tick(S)
                if o.dead:
                    o.erase(B)
                    l.remove(o)

        #HERE IS THE GLITTER
        #self.glitter.update(S)
        #self.glitter.add(self.shotobjs, 1.0)

        for l in objects:
            for o in l:
                o.draw(G)


        self.hud.draw()

    def background(self, area):
        return self.bgfill(0, area)
        #return self.bgfill((70,70,70), area)

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
        if self.levelnum >= 10:
            gamehelp.help("spikes", self.player.pos)
        if self.levelnum >= 30:
            gamehelp.help("secretspikes", self.player.pos)

        if len(self.asteroidobjs):
            gamehelp.help("asteroids", self.asteroidobjs[0].rect.center)


    def normal_tick(self):
        #fire the guards
        shootchance = game.guard_fire * self.speedadjust
        if self.player.active and random.random() < shootchance:
            self.powerupcount += 0.3
            baddy = random.choice(self.guardobjs)
            baddy.fire() #only requests a shot
        for baddy in self.guardobjs:
            shotspot, shotdir = baddy.shotinfo()
            if shotspot:
                s = objshot.Shot(shotspot, shotdir)
                self.shotobjs.append(s)
                snd.play('shoot', 1.0, shotspot[0])

        #add a powerup if ready
        if self.powerupcount >= game.powerupwait:
            self.powerupcount = 0.0
            p = objpowerup.newpowerup(self.levelnum)
            self.powerupobjs.append(p)
            snd.play('spring', 0.6)
            gamehelp.help("powerup", p.rect.topleft)
        if self.grabbedboxes >= 50:
            self.grabbedboxes = 0
            if game.comments >= 1:
                self.textobjs.append(objtext.Text(game.Complements[self.complement]))
            self.complement = (self.complement + 1) % len(game.Complements)
        elif self.grabbedboxes >= 20:
            self.numdeaths = 0

        self.tickleveltime(self.speedadjust)

        playerrect = self.player.rect.inflate(-1, -1)
        playercollide = playerrect.colliderect
        #collide player to boxes
        if self.touchingsecretspike:
            if not playercollide(self.touchingsecretspike.rect):
                #self.boxobjs.remove(self.touchingsecretspike)
                self.spikeobjs.append(objbox.Spike(self.touchingsecretspike.rect.topleft))
                self.boxobjs.remove(self.touchingsecretspike)
                self.touchingsecretspike = None
        for b in self.boxobjs:
            status = b.playercollide(playerrect)
            if status:
                self.grabbedboxes += 1
                self.powerupcount += 0.6
                if b in self.secretspikes:
                    self.touchingsecretspike = b
                    self.secretspikes.remove(b)
                    snd.play('klank2', 0.7, self.player.rect.centerx)
                elif status == 1:
                        self.powerupcount += 0.3
                        self.boxobjs.remove(b)
                        self.popobjs.append(b)
        #collide player to powerups
        for p in self.powerupobjs:
            if playercollide(p.rect):
                p.dead = 1
                effect = p.effect()
                if game.comments >= 2:
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
        #collide player to spikes
        for s in self.spikeobjs:
            if s.armed and playercollide(s.rect):
                s.dead = 1
                self.changestate('playerdie')
                hitbullet = 1
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
        game.player.lives += 1
        snd.play('explode', 1.0, self.player.rect.centerx)
        #self.explode = objexplode.Explode(self.player.rect.center, self.player.move)
        #self.staticobjs.append(self.explode)
        self.staticobjs.extend(objexplode.superexplode(self.player.rect.center, self.player.move))
        self.explode = self.staticobjs[-1]
        self.poptime = 3
        self.player.dead = 1
        self.player.active = 0
        self.grabbedboxes = 0
        self.numdeaths += 1
        if game.comments >= 2 and len(self.boxobjs) <= 2:
            self.textobjs.append(objtext.Text('Doh, so close'))
        elif game.comments >= 2 and self.numdeaths > 1:
            self.textobjs.append(objtext.Text(game.Insults[self.complement]))
            self.complement = (self.complement + 1) % len(game.Insults)
        for effect in self.powereffects:
            effect.dead = 1
        for b in self.guardobjs:
            b.nofire()


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
                if game.comments >= 2 and not self.lives_left:
                    self.textobjs.append(objtext.Text("Last Ship, Don't Blow It"))
            else:
                self.changestate('gameover')
        self.tickleveltime(self.speedadjust * 1.5)
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
        collide = self.teleport.rect.inflate(12, 12).colliderect
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
        if self.teleport.rocksclear:
            self.tickleveltime(self.speedadjust)

    def playerstart_end(self):
        input.resetexclusive()
        input.postactive()
        #del self.teleport


#level start
    def levelstart_start(self):
        self.skipping = game.timeleft > 0.0
        self.levelnum += 1
        del self.boxobjs[:]
        self.newboxes, self.startpos, msg, num = levels.makelevel(self.levelnum)
        random.shuffle(self.newboxes)
        self.calcboxes = num
        self.addtime = 2
        if game.clock.get_fps() < 25:
            self.addtime = 1
        self.hud.drawlevel(self.levelnum)
        if game.comments >= 2:
            self.textobjs.append(objtext.Text(msg))
        self.grabbedboxes = 0
        self.numdeaths = 0
        for b in self.guardobjs:
            b.nofire()

        if self.levelnum > game.player.score:
            game.player.score = self.levelnum
        if not self.newcontinue and game.player.start_level() > self.startlevel:
            self.newcontinue = 1

        for i in range(levels.numrocks(self.levelnum) - len(self.asteroidobjs)):
            self.asteroidobjs.append(objasteroid.Asteroid())

        for p in self.powerupobjs:
            p.extendtime()

        if self.skipping: self.skiptime = 20

        #teleport in dead guards
        for g in self.guardobjs:
            if g.killed == 1:
                self.smokeobjs.append(objguard.TeleGuard(g))
                g.killed = 2

        #make spikes
        if self.levelnum >= 30:
            numspikes = min(int((self.levelnum-30)/5) + 1, len(self.newboxes)-5)
            self.secretspikes = self.newboxes[-numspikes:]
        elif self.levelnum >= 10:
            numspikes = int((self.levelnum-10)/7) + 1
            spikes = self.newboxes[-numspikes:]
            self.newboxes = self.newboxes[:-numspikes]
            for b in spikes:
                s = objbox.Spike(b.rect.topleft)
                self.spikeobjs.append(s)
            self.secretspikes = []
            self.touchingsecretspike = None
        else:
            self.secretspikes = []
            self.touchingsecretspike = None

        #rotate music
        if pygame.time.get_ticks() - self.songtime > game.musictime:
            songs = list(Songs)
            songs.remove(self.song)
            self.song = random.choice(songs)
            snd.playmusic(*self.song)
            self.songtime = pygame.time.get_ticks()

    def levelstart_tick(self):
        self.addtime -= 1
        if not self.addtime:
            self.addtime = 2
            if self.newboxes:
                b = self.newboxes.pop()
                self.boxobjs.append(b)
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
        pct = pct * .92
        game.guard_fire = .01 + pct * game.fire_factor
        if len(self.boxobjs):
            game.timetick = (1000.0 / (self.calcboxes * game.timefactor))
        else:
            game.timetick = 5.0
        if self.levelnum <= 1: game.timetick = 4.0
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
        if game.comments >= 1 and self.grabbedboxes >= 36:
            self.textobjs.append(objtext.Text(game.Complements[self.complement]))
            self.complement = (self.complement + 1) % len(game.Complements)
        for s in self.spikeobjs:
            s.dead = 1
            self.popobjs.append(objpopshot.PopShot(s.rect.center))
        #boxes may be left if the player cheated
        for b in self.boxobjs:
            b.erase(self.background)
        del self.boxobjs[:]


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
        game.player.skips += 1
        self.poptime = 2
        if game.clock.get_fps() < 25:
            self.poptime = 1
        if game.comments >= 1:
            self.textobjs.append(objtext.Text('Level Skipped'))
        self.skiptime = 25
        for s in self.spikeobjs:
            s.dead = 1
            self.popobjs.append(objpopshot.PopShot(s.rect.center))

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
                    b.pop()
                    self.boxobjs.remove(b)
                    self.popobjs.append(b)
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
        for g in self.guardobjs:
            if g.killed == 1:
                self.smokeobjs.append(objguard.TeleGuard(g))
                g.killed = 2


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

        self.runobjects([self.smokeobjs, self.guardobjs])

    def gamestart_end(self):
        if game.comments >= 1:
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
            for g in self.guardobjs:
                if not g.killed:
                    g.killed = 1
                    explode = objexplode.Explode(g.rect.center)
                    self.staticobjs.append(explode)
                    #argh, force a cleanup
                    self.background(g.lastrect)
                    gfx.dirty(g.lastrect)

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
                import gamename
                nexthandler = gamename.GameName(nexthandler)
        if self.newcontinue:
            if not game.player in players.players:
                players.players.append(game.player)

            #add a highscore handler into these chains
            if not game.player.name:
                import gamename
                nexthandler = gamename.GameName(nexthandler)

        game.handler = nexthandler



