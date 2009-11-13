#!/usr/bin/env python

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
"""
Solarwolf, created by Pete Shinners.
"""

import sys, os



#these directories will be used if solarwolf cannot find
#the directories in the location of the main program
if sys.platform == "win32":
    DATADIR = "C:\\Program Files\\Solarwolf"
    CODEDIR = "C:\\Program Files\\Solarwolf\\code"
else:
    DATADIR = "/usr/share/games/solarwolf"
    CODEDIR = "/usr/lib/games/solarwolf"



def main():
    #figure out our directories
    global DATADIR, CODEDIR
    localpath = os.path.split(os.path.abspath(sys.argv[0]))[0]
    testdata = localpath
    testcode = os.path.join(localpath, 'code')
    if os.path.isdir(os.path.join(testdata, 'data')):
        DATADIR = testdata
    if os.path.isdir(testcode):
        CODEDIR = testcode

    #apply our directories and test environment
    os.chdir(DATADIR)
    sys.path.insert(0, CODEDIR)
    checkdependencies()

    #install pychecker if debugging
    game = None
    try:
        import game
        if game.DEBUG >= 2:
            import pychecker.checker
            print 'Pychecker Enabled'
    except ImportError, m:
        pass

    #run game and protect from exceptions
    try:
        import main, pygame
        main.main(sys.argv)
    except KeyboardInterrupt:
        print 'Keyboard Interrupt (Control-C)...'
    except:
        #should wait on any threading
        #never seen this happen though
        if game and game.thread:
            game.threadstop = 1
            while game.thread:
                pygame.time.wait(10)
                print 'waiting on thread...'
        exception_handler()
        if not game or game.DEBUG:
            raise




def checkdependencies():
    "only returns if everything looks ok"
    msgs = []

    #make sure this looks like the right directory
    if not os.path.isdir(CODEDIR):
        msgs.append('Cannot locate SolarWolf modules')
    if not os.path.isdir('data'):
        msgs.append('Cannot locate SolarWolf data files')

    #first, we need python >= 2.1
    if int(sys.version[0]) < 2:
        errorbox('Requires Python-2.1 or Greater')

    #is correct pygame found?
    try:
        import pygame
        if pygame.ver < '1.6.1':
            msgs.append('Requires Pygame-1.6.1 or Greater, You Have ' + pygame.ver)
    except ImportError:
        msgs.append("Cannot import Pygame, install version 1.6.1 or higher")
        pygame = None

    #check that we have FONT and IMAGE
    if pygame:
        if not pygame.font:
            msgs.append('Pygame requires the SDL_ttf library, not available')
        if not pygame.image or not pygame.image.get_extended():
            msgs.append('Pygame requires the SDL_image library, not available')

    if msgs:
        msg = '\n'.join(msgs)
        errorbox(msg)


def errorbox(message):
    message = str(message)
    if not message: message = 'Error'
    import errorbox
    errorbox.errorbox("Solarwolf Error", message)
    sys.stderr.write('ERROR: ' + message + '\n')
    raise SystemExit

def exception_handler():
    import traceback
    type, info, trace = sys.exc_info()
    tracetop = traceback.extract_tb(trace)[-1]
    tracetext = 'File %s, Line %d' % tracetop[:2]
    if tracetop[2] != '?':
        tracetext += ', Function %s' % tracetop[2]
    exception_message = '%s:\n%s\n\n%s\n"%s"'
    message = exception_message % (str(type), str(info), tracetext, tracetop[3])
    if type not in (KeyboardInterrupt, SystemExit):
        import errorbox
        errorbox.errorbox("Solarwolf Error", message)
        sys.stderr.write('ERROR: ' + message + '\n')
        raise SystemExit
 


if __name__ == '__main__': main()
