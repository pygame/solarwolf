#!/usr/bin/env python
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

    # first try to get the path from the solarwolf package.
    try:
        import solarwolf
        if type(solarwolf.__path__) == list:
            localpath = os.path.abspath(solarwolf.__path__[0])
        else:
            localpath = os.path.abspath(solarwolf.__path__._path[0])
    except ImportError:
        localpath = os.path.split(os.path.abspath(sys.argv[0]))[0]

    testdata = localpath
    testcode = os.path.join(localpath, '.')

    if os.path.isdir(os.path.join(testdata, 'data')):
        DATADIR = testdata
    if os.path.isdir(testcode):
        CODEDIR = testcode

    #apply our directories and test environment
    os.chdir(DATADIR)
    sys.path.insert(0, CODEDIR)
    checkdependencies()

    #install pychecker if debugging
    try:
        import game
        if game.DEBUG >= 2:
            import pychecker.checker
            print('Pychecker Enabled')
    except ImportError:
        pass

    #run game and protect from exceptions
    try:
        import main, pygame
        main.main(sys.argv)
    except KeyboardInterrupt:
        print('Keyboard Interrupt (Control-C)...')
    except:
        #must wait on any threading
        if game.thread:
            game.threadstop = 1
            while game.thread:
                pygame.time.wait(10)
                print('waiting on thread...')
        exception_handler()
        if game.DEBUG:
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
        if pygame.ver < '1.5.6':
            msgs.append('Requires Pygame-1.5.6 or Greater, You Have ' + pygame.ver)
    except ImportError:
        msgs.append("Cannot import Pygame, install version 1.5.6 or higher")
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



#Pretty Error Handling Code...

def __windowsbox(title, message):
    raise ImportError #the MessageBox command is crashing!
    import win32ui, win32con
    win32ui.MessageBox(message, title, win32con.MB_ICONERROR)

def __wxpythonbox(title, message):
    import wxPython.wx as wx
    class LameApp(wx.wxApp):
        def OnInit(self): return 1
    app = LameApp()
    dlg = wx.wxMessageDialog(None, message, title, wx.wxOK|wx.wxICON_EXCLAMATION)
    dlg.ShowModal()
    dlg.Destroy()

def __tkinterbox(title, message):
    import tkinter, tkinter.messagebox
    tkinter.Tk().wm_withdraw()
    tkinter.messagebox.showerror(title, message)


def __pygamebox(title, message):
    try:
        import pygame
        pygame.quit() #clean out anything running
        pygame.display.init()
        pygame.font.init()
        screen = pygame.display.set_mode((460, 140))
        pygame.display.set_caption(title)
        font = pygame.font.Font(None, 18)
        foreg, backg, liteg = (0, 0, 0), (180, 180, 180), (210, 210, 210)
        ok = font.render('Ok', 1, foreg, liteg)
        okbox = ok.get_rect().inflate(200, 10)
        okbox.centerx = screen.get_rect().centerx
        okbox.bottom = screen.get_rect().bottom - 10
        screen.fill(backg)
        screen.fill(liteg, okbox)
        screen.blit(ok, okbox.inflate(-200, -10))
        pos = [10, 10]
        for text in message.split('\n'):
            if text:
                msg = font.render(text, 1, foreg, backg)
                screen.blit(msg, pos)
            pos[1] += font.get_height()
        pygame.display.flip()
        stopkeys = pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER
        while 1:
            e = pygame.event.wait()
            if e.type == pygame.QUIT or \
                       (e.type == pygame.KEYDOWN and e.key in stopkeys) or \
                       (e.type == pygame.MOUSEBUTTONDOWN and okbox.collidepoint(e.pos)):
                break
        pygame.quit()
    except pygame.error:
        raise ImportError

handlers = __pygamebox, __tkinterbox, __wxpythonbox, __windowsbox

def __showerrorbox(message):
    title = os.path.splitext(os.path.split(sys.argv[0])[1])[0]
    title = title.capitalize() + ' Error'
    for e in handlers:
        try:
            e(title, message)
            break
        except (ImportError, NameError, AttributeError):
            pass

def errorbox(message):
    message = str(message)
    if not message: message = 'Error'
    __showerrorbox(message)
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
        __showerrorbox(message)
    raise



if __name__ == '__main__': main()
