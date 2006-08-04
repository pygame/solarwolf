#!/usr/bin/env python 
"""
Solarwolf has been created by Pete Shinners.
The original Solarwolf was released in May, 2001.
About a year later this exciting new version is available.
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

    try:
        import game
        if game.DEBUG >= 2:
            import pychecker.checker
            print 'Pychecker Enabled'
    except ImportError, m:
        print 'No Pychecker', m

    try:
        import main, pygame
        main.main(sys.argv)
    except KeyboardInterrupt:
        print 'Keyboard Interrupt (Control-C)...'
    except:
        #must wait on any threading
        if game.thread:
            game.threadstop = 1
            while game.thread:
                pygame.time.wait(10)
                print 'waiting on thread...'
        exception_handler()
        if game.DEBUG:
            raise




def checkdependencies():
    "only returns if everything looks ok"
    msgs = []

    #make sure this looks like the right directory
    if not os.path.isdir('code'):
        msgs.append('Cannot locate SolarWolf modules (code subdirectory)')
    if not os.path.isdir('data'):
        msgs.append('Cannot locate SolarWolf data files (data subdirectory)')

    #first, we need python >= 2.0
    if int(sys.version[0]) < 2:
        errorbox('Requires Python-2.0 or Greater')
    
    #is correct pygame found?
    try:
        import pygame
        if pygame.ver < '1.5':
            msgs.append('Requires Pygame-1.5 or Greater, You Have ' + pygame.ver)
    except ImportError:
        msgs.append("Cannot import Pygame, install version 1.4 or higher")

    #check pygame version and that we have FONT and IMAGE
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
    import Tkinter, tkMessageBox
    Tkinter.Tk().wm_withdraw()
    tkMessageBox.showerror(title, message)

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
        stepkeys = pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN
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
