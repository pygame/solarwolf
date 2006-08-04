"""main module, starts game and main loop"""

import sys
import pygame
import game, gfx, snd, input
import allmodules
import players


#at this point, all needed pygame modules should
#be imported, so they can be initialized at the
#start of main()



def main(args):
    try:
        gamemain(args)
    except KeyboardInterrupt:
        print 'Keyboard Interrupt (Control-C)...'
        print 'Exiting'


def gamemain(args):
    #initialize all our code (not load resources)
    pygame.init()
    game.clock = pygame.time.Clock()

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

    #set timer to control stars..
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    #main game loop
    lasthandler = None
    while game.handler:
        handler = game.handler
        if handler != lasthandler:
            lasthandler = handler
            if hasattr(handler, 'starting'):
                handler.starting()
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                fps = game.clock.get_fps()
                #print 'FRAMERATE: %f fps' % fps
                gfx.starobj.recalc_num_stars(fps)
                continue
            inputtype = input.translate(event)
            if inputtype:
                handler.input(inputtype)
            elif event.type == pygame.QUIT:
                game.handler = None
                break
            handler.event(event)
        handler.run()
        game.clockticks = game.clock.tick(40)
        gfx.update()
        while not pygame.display.get_active():
            pygame.time.delay(100)
            pygame.event.pump()

        #pygame.time.wait(18)

    #game is finished at this point, do any
    #uninitialization needed
    players.save_players()
    pygame.quit()



