"""tries its hardest to display a message box on the screen"""

import sys


def __windows(type, title, message):
    #this is tested and works
    raise ImportError #the MessageBox command is crashing!
    import win32ui, win32con
    win32ui.MessageBox(message, title, win32con.MB_ICONERROR)


def __wxpython(type, title, message):
    #this is tested and works
    from wxPython.wx import *
    class LameApp(wxApp):
        def OnInit(self): return 1
    app = LameApp()
    dlg = wxMessageDialog(None, message, title, wxOK|wxICON_EXCLAMATION)
    dlg.ShowModal()
    dlg.Destroy()


def __gtk(type, title, message):
    #this is totally untested
    import GtkExtra
    GtkExtra.message_box(title, message, ['Ok'])
   

def __tkinter(type, title, message):
    #this is tested and works (thanks e@ircnet #python)
    import Tkinter, tkMessageBox
    Tkinter.Tk().wm_withdraw()
    tkMessageBox.showerror(title, message)


def __pygame(type, title, message):
    try:
        import pygame, pygame.font
        from pygame.locals import *
        pygame.quit() #clean out anything running
        pygame.display.init()
        pygame.font.init()
        screen = pygame.display.set_mode((460, 140))
        pygame.display.set_caption(title)
        font = pygame.font.Font(None, 18)
        foreg = 0, 0, 0
        backg = 200, 200, 200
        liteg = 255, 255, 255
        ok = font.render('Ok', 1, foreg)
        screen.fill(backg)
        okbox = ok.get_rect().inflate(20, 10)
        okbox.centerx = screen.get_rect().centerx
        okbox.bottom = screen.get_rect().bottom - 10
        screen.fill(liteg, okbox)
        screen.blit(ok, okbox.inflate(-20, -10))
        pos = [20, 20]
        for text in message.split('\n'):
            msg = font.render(text, 1, foreg)
            screen.blit(msg, pos)
            pos[1] += font.get_height()

        pygame.display.flip()
        while 1:
            e = pygame.event.wait()
            if e.type == QUIT or e.type == MOUSEBUTTONDOWN or \
                       (e.type == KEYDOWN and e.key in (K_ESCAPE, K_SPACE, K_RETURN)):
                break
        pygame.quit()
    except pygame.error:
        raise ImportError


def __stdout(type, title, message):
    text = type.upper() + ': ' + title + '\n' + message
    print text



handlers = __gtk, __tkinter, __wxpython, __windows, __pygame

def error(title, message):
    for e in handlers:
        try:
            e('error', title, message)
            break
        except (ImportError, NameError):
            pass
    __stdout('error', title, message)
    raise SystemExit



if __name__ == '__main__': #test the error box
    error("Testing", "This is only a test.\nHad this been " + \
          "a real emergency, you would be very afraid." )
