"""errorbox, by Pete Shinners

Tries multiple python GUI libraries to display an error box
on the screen. No matter what is successful, the error will also
be sent to stdout. For GUI platforms, this can be a lot nicer than
opening a shell with errors dumped into it.

Call the "errorbox()" function with an error title and error message.

The different GUI libraries will leave the program in undefined
states, so this function will never return, but instead end the
program when the error has been dismissed. That makes this only
useful for errors, and not general message boxes.

Feel free to perhaps add some GUI handlers, as well as enhance
any that are here. They have all been tested on their appropriate
platforms.

There is even a decent pygame handler, if all else fails.

Use it to report things like missing modules (image, numeric, etc?).
Perhaps pygame raised an exception while initializing. This little
messagebox can sure be a lot nicer than a stack trace. ;]
"""



def errorbox(title, message):
    "attempt to error with a gui"
    global handlers
    __stdout(title, message)
    for e in handlers:
        try:
            e(title, message)
            break
        except (ImportError, NameError): pass
    raise SystemExit



def __pyqt4(title, message):
    from PyQt4 import QtGui
    app = QtGui.QApplication(["Error"])
    QtGui.QMessageBox.critical(None, title, message)


def __wxpython(title, message):
    from wxPython.wx import wxApp, wxMessageDialog, wxOK, wxICON_EXCLAMATION
    class LameApp(wxApp):
        def OnInit(self): return 1
    app = LameApp()
    dlg = wxMessageDialog(None, message, title, wxOK|wxICON_EXCLAMATION)
    dlg.ShowModal()
    dlg.Destroy()


def __tkinter(title, message):
    import tkinter, tkinter.messagebox
    tkinter.Tk().wm_withdraw()
    tkinter.messagebox.showerror(title, message)


def __pygame(title, message):
    try:
        import pygame, pygame.font
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
            if (e.type == pygame.QUIT or e.type == pygame.MOUSEBUTTONDOWN or
                        pygame.KEYDOWN and e.key
                        in (pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN)):
                break
        pygame.quit()
    except pygame.error:
        raise ImportError


def __stdout(title, message):
    text = 'ERROR: ' + title + '\n' + message
    print(text)

handlers = __pyqt4, __tkinter, __wxpython, __pygame


#test the error box
if __name__ == '__main__':
    errorbox("Testing", "This is only a test.\nHad this been " + \
          "a real emergency, you would be very afraid." )
