#!/usr/bin/env python

"""
SolarWolf, the game
by Pete Shinners with the amazing pygame
"""
import sys, os


def main():

    #make sure we're in the correct directory
    fullpath = os.path.abspath(sys.argv[0])
    dir = os.path.split(fullpath)[0]
    os.chdir(dir)

    #add our code to the python path    
    sys.path.insert(0, 'code')
    
    checkdependencies()

    import main
    main.main(sys.argv)




def checkdependencies():
    "only returns if everything looks ok"
    #first, we need python >= 2.0
    import sys
    if int(sys.version[0]) < 2:
        raise SystemExit, "SolarWolf Requires Python 2.0 or Higher"
    
    #first see if we a few some solarwolf modules
    check = 'messagebox', 'game'
    try:
        imps = []
        for c in check:
            imps.append(__import__(c))
    except ImportError:
        raise SystemExit, "Cannot Import SolarWolf Modules"
    errorbox = imps[0].error

    #check pygame version and that we have FONT and IMAGE
    msgs = []
    try:
        from pygame.version import ver
        if ver < 1.0: raise ImportError
    except ImportError:
        msgs.append('Requires Pygame-1.0 or Greater')
    try: import pygame.image
    except ImportError:
        msgs.append('Requires the Pygame Image Module')
    try: import pygame.font
    except ImportError:
        msgs.append('Requires the Pygame Font Module')
    if msgs:
        msg = '\n'.join(msgs)
        errorbox(msg)

    #make sure this looks like the right directory
    if not os.path.isdir('data'):
        errorbox('Cannot locate SolarWolf data files')



if __name__ == '__main__': main()
