"""main module, starts game and main loop"""

try:
    import sys
    import pygame
    import game, gfx, snd, input
    import allmodules
    import FpsClock
    import players
#except ImportError, msg:
#    import messagebox
#    messagebox.error('Error Initializing', msg.args[0])
#    raise
except RuntimeError: raise

#at this point, all needed pygame modules should
#be imported, so they can be initialized at the
#start of main()



def main(args):
    try:
        gamemain(args)
    except KeyboardInterrupt:
        print 'Keyboard Interrupt (Control-C)...'
        print 'Exiting'


class MyFpsClock(FpsClock.FpsClock):
    def report(self):
        #FpsClock.FpsClock.report(self)
        if gfx.starobj: gfx.starobj.recalc_num_stars(self.current_fps)


def gamemain(args):
    #initialize all our code (not load resources)
    pygame.init()
    game.clock = MyFpsClock(40, 1)

    size = 800, 600
    full = '-window' not in args
    gfx.initialize(size, full)
    pygame.display.set_caption('SolarWolf')        

    if not '-nosound' in args:
        snd.initialize()
    input.init()
    players.load_players()

    #create the starting game handler
    from gameinit import GameInit
    from gamefinish import GameFinish
    game.handler = GameInit(GameFinish(None))

    
    #main game loop
    lasthandler = None
    while game.handler:
        handler = game.handler
        if handler != lasthandler:
            lasthandler = handler
            if hasattr(handler, 'starting'):
                handler.starting()
        for event in pygame.event.get():
            inputtype = input.translate(event)
            if inputtype:
                handler.input(inputtype)
            elif event.type == pygame.QUIT:
                game.handler = None
                break
            handler.event(event)
        handler.run()
        game.clock.tick() #note, tick can cause stars to erase
        gfx.update()
        while not pygame.display.get_active():
            pygame.time.delay(100)
            pygame.event.pump()

        #pygame.time.delay(18)

    #game is finished at this point, do any
    #uninitialization needed
    players.save_players()
    pygame.quit()



