"gameplay handler. for the main part of the game"

import pygame
from pygame.locals import *
import random, math

import game, gfx, input, snd
import objship, objbox, objguard, objshot, objexplode, objtele
import objpopbox, objpopshot, objtext, objsmoke, objwarp
import levels, hud, players

#num of insults must match num of complements
Complements = (
    'You\'re on fire!',
    'Not too shabby',
    'Keep it up!',
    'Looking great!',
    'Use the force, luke!',
    'Hotshot',
    'Make momma proud',
    'Rad-o-cool',
    'Too hot to handle'
)
Insults = (
    'Try missing the bullets',
    'Not so good',
    'Ouch',
    'Look away',
    'Rookie',
    'It hurts, it hurts',
    'Both hands on the wheel',
    'Choke Choke',
    'Don\'t quit that day job',
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
        self.popobjs = []
        self.textobjs = []
        self.smokeobjs = []
        self.guardobjs = [objguard.Guard(x) for x in range(4)]
        self.objlists = [self.boxobjs, self.shotobjs, self.popobjs, self.smokeobjs,
                         self.guardobjs, self.staticobjs, self.textobjs]
        self.hud = hud.HUD()

        self.state = ''
        self.statetick = self.dummyfunc
        self.lives_left = 0
        self.shotsfired = 0
        self.numdeaths = 0
        self.complement = random.randint(0, len(Complements)-1)

        self.lasttick = pygame.time.get_ticks()        
        self.speedadjust = 1.0

        self.changestate('gamestart')

        self.input_mapping = {
            input.ABORT:  (self.userquit, []),
            input.UP:     (self.player.cmd_up, []),
            input.DOWN:   (self.player.cmd_down, []),
            input.LEFT:   (self.player.cmd_left, []),
            input.RIGHT:  (self.player.cmd_right, []),
            input.PRESS:  (self.player.cmd_turbo, [1]),
            input.RELEASE:(self.player.cmd_turbo, [0]),
        }

        self.bgfill = gfx.surface.fill


    def starting(self):
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
        func, args = self.input_mapping[i]
        func(*args)

    def event(self, e):
        pass

    def run(self):
        now = pygame.time.get_ticks()
        diff = now - self.lasttick
        ratio = float(diff) / game.clockticks
        self.speedadjust = max(ratio, 1.0)
        self.lasttick = now
        
        self.statetick()


    def runobjects(self, objects):        
        G, B, S = gfx, self.background, self.speedadjust
        gfx.updatestars(B, G)
        for l, o in [(l, o) for l in objects for o in l]:
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
        if game.timeleft:
            game.timeleft = game.timeleft - game.timetick * speedadjust
            if game.timeleft < 0:
                game.timeleft = 0.0



#normal play
    def normal_start(self):
        self.clocks = 0
        
    def normal_tick(self):
        if not self.player.active:
            self.player.start((100, 100))

        #fire the guards
        shootchance = game.guard_fire * self.speedadjust
        if self.player.active and random.random() < shootchance:
            baddy = self.guardobjs[random.randint(0,3)]
            if not baddy.reloading:
                baddy.reloading = objguard.guard_loadtime
        for baddy in self.guardobjs:
            if not baddy.fireme: continue
            shotspot, shotdir = baddy.shotinfo()
            s = objshot.Shot(shotspot, shotdir)
            self.shotobjs.append(s)
            snd.play('shoot', 1.0, shotspot[0])
            self.shotsfired += 1
            if self.shotsfired == 40:
                self.textobjs.append(objtext.Text(Complements[self.complement]))
                self.complement = (self.complement + 1) % len(Complements)
                self.shotsfired = 10

        self.tickleveltime(self.speedadjust)

        playerrect = self.player.rect.inflate(-1, -1)
        for b in self.boxobjs:
            if b.playercollide(playerrect):
                b.dead = 1
                self.popobjs.append(objpopbox.PopBox(b.rect.center))
        playerrect = playerrect.inflate(-3, -3)
        for s in self.shotobjs:
            if playerrect.colliderect(s.rect):
                s.dead = 1
                self.player.dead = 1
                self.player.active = 0
                self.changestate('playerdie')

        if not self.boxobjs:
            self.changestate('levelend')

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
        self.shotsfired = 0
        self.numdeaths += 1
        if self.numdeaths > 1:
            self.textobjs.append(objtext.Text(Insults[self.complement]))
            self.complement = (self.complement + 1) % len(Insults)
        if len(self.boxobjs) <= 2:
            self.textobjs.append(objtext.Text('Doh, so close'))
        
        
    def playerdie_tick(self):
        game.timeleft = max(game.timeleft - 10.0, 0.0)
        self.poptime -= 1
        if not self.poptime:
            self.poptime = 3
            if self.shotobjs:
                s = self.shotobjs[0]
                s.dead = 1
                self.popobjs.append(objpopshot.PopShot(s.rect.center))
        if self.explode.dead and not self.popobjs and not game.timeleft:
            if self.lives_left:
                self.lives_left -= 1
                self.hud.drawlives(self.lives_left)
                self.changestate('playerstart')
                if not self.lives_left:
                    self.textobjs.append(objtext.Text("Last ship, don't blow it"))
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
        self.teleport = objtele.Tele(self.startpos)
        self.popobjs.append(self.teleport)
        self.shotsfired = 0

    def playerstart_tick(self):
        #when animations done
        if self.teleport.dead:
            self.changestate('normal')
            self.player.start(self.startpos)
            self.staticobjs.append(self.player)
        self.runobjects(self.objlists)

    def playerstart_end(self):
        #this needs to handle all inputs, not just keyboard
        turbo = pygame.key.get_pressed()[K_SPACE]
        self.player.cmd_turbo(turbo)
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
        self.textobjs.append(objtext.Text(msg))
        self.shotsfired = 0
        self.numdeaths = 0

        if self.levelnum > game.player.score:
            game.player.score = self.levelnum
        if not self.newcontinue and game.player.start_level() > self.startlevel:
            self.newcontinue = 1

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
        game.guard_fire = .01 + math.log(self.levelnum+1)* .022
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
            game.timeleft = max(game.timeleft - 4.0, 0.0)
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
            if not self.ticks % 4 and self.levelnum < self.startlevel-1:
                self.levelnum += 1
                self.hud.drawlevel(self.levelnum)
            if not self.ticks % 10 and self.lives_left < game.start_lives:
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
                self.final_game_end()              
        self.runobjects(self.objlists)


    def final_game_end(self):
        nexthandler = self.prevhandler
        if self.gamewon:
            import gamewin
            nexthandler = gamewin.GameWin(nexthandler)
            players.make_winner(game.player)
        if self.newcontinue:
            if not game.player in players.players:
                players.players.append(game.player)

            #add a highscore handler into these chains
            if not game.player.name:
                import gamename
                game.handler = gamename.GameName(nexthandler)
                return

        game.handler = nexthandler



