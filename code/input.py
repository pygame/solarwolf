"""Translate pygame events to controls, part of SOLARWOLF."""
# Portions Copyright (C) 2002 Aaron "APS" Schlaegel, LGPL, see lgpl.txt

import pygame.joystick
from pygame.locals import *
import time, sys, os, pickle, tempfile
import game, snd

ScreenshotNum = 1

# control constants
DEFAULT   = 0
UP        = 1
DOWN      = 2
LEFT      = 3
RIGHT     = 4
PRESS     = 5
ABORT     = 6

# axis norm constants, add 2 for every axis
AXISLESS  = 0
AXISMORE  = 1

# hat norm constants, add 4 for every hat
HATSTART = HATUP = 0
HATLEFT = 1
HATRIGHT = 2
HATDOWN = 3

FINISHMUSIC = USEREVENT+3

#translation tables
translations_default = {
    KEYDOWN: {
        K_UP: UP,
        K_DOWN: DOWN,
        K_LEFT: LEFT,
        K_RIGHT: RIGHT,
        K_RETURN: PRESS,
        K_SPACE: PRESS,
        K_KP8: UP,
        K_KP2: DOWN,
        K_KP4: LEFT,
        K_KP6: RIGHT,
        K_KP5: DOWN,
        K_ESCAPE: ABORT,
        K_DELETE: ABORT,
        K_BREAK: ABORT,
        #vi keys
        K_h: LEFT,
        K_j: DOWN,
        K_k: UP,
        K_l: RIGHT,
    },
    NOEVENT: {
#        KEYDOWN: PRESS,
#        JOYAXISMOTION: None,
#        JOYBUTTONDOWN: PRESS,
#        JOYHATMOTION: None
    },
    JOYAXISMOTION: {
        AXISLESS + 0: LEFT,
        AXISMORE + 0: RIGHT,
        AXISLESS + 2: UP,
        AXISMORE + 2: DOWN,
        AXISLESS + 4: LEFT,
        AXISMORE + 4: RIGHT,
        AXISLESS + 6: UP,
        AXISMORE + 6: DOWN,
    },
    JOYBUTTONDOWN: {
        1: PRESS,
        2: PRESS,
        3: PRESS,
        12: UP,
        14: DOWN,
        15: LEFT,
        13: RIGHT,
    },
    JOYHATMOTION: {
        HATUP + 0: UP,
        HATDOWN + 0: DOWN,
        HATLEFT + 0: LEFT,
        HATRIGHT + 0: RIGHT,
    }
}

hat_direction_text = {
    HATUP: "Up", HATLEFT: "Left", HATRIGHT: "Right", HATDOWN: "Down"
}

actions_text = {
    UP: "Up",
    DOWN: "Down",
    LEFT: "Left",
    RIGHT: "Right",
    PRESS: "Turbo",
    ABORT: "Abort",
}

actions_order = [
    UP, DOWN, LEFT, RIGHT, PRESS, ABORT
]

joystick = None
lastaxisvalue = []

translations = {}

joystick = None
lastaxisvalue = []
lasthatvalue = []
exclusivedict = {}
Cheatstring = ''

def init():
    "init the joystick"
    global joystick
    global lastaxisvalue
    global lasthatvalue
    try:
        num = pygame.joystick.get_count()
        if num > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            lastaxisvalue = [None]*joystick.get_numaxes()
            lasthatvalue = [[None, None]]*joystick.get_numhats()

    except pygame.error:
        joystick = None



def postactive():
    keystate = pygame.key.get_pressed()
    for key in range (len(keystate)):
        if keystate[key]:
            #I don't know how to get unicode
            pygame.event.post(pygame.event.Event(KEYDOWN, {'key': key, 'mod': pygame.key.get_mods()}))
    if joystick:
        for button in range(joystick.get_numbuttons()):
            if joystick.get_button(button):
                pygame.event.post(pygame.event.Event(JOYBUTTONDOWN, {'joy': joystick.get_id(), 'button': button}))
        for hat in range(joystick.get_numhats()):
            value = joystick.get_hat(hat)
            if 0 != value[0] or 0 != value[1]:
                pygame.event.post(pygame.event.Event(JOYHATMOTION, {'joy': joystick.get_id(), 'hat': hat, 'value': value}))
        for axis in range(joystick.get_numaxes()):
            lastaxisvalue[axis] = None
            value =  joystick.get_axis(axis)
            pygame.event.post(pygame.event.Event(JOYAXISMOTION, {'joy': joystick.get_id(), 'axis': axis, 'value': value}))

def resetexclusive():
    global exclusivedict
    exclusivedict.clear()

def exclusive(list, i):
    global exclusivedict
    thislist = str(list)
    if i.translated in list:
        if not exclusivedict.has_key(thislist):
            exclusivedict[thislist] = {}
        table = exclusivedict[thislist]
        if i.release:
            if not table.has_key(i.translated):
                table[i.translated] = 0
            else:
                table[i.translated] -= 1
        else:
            if not table.has_key(i.translated):
                table[i.translated] = 1
            else:
                table[i.translated] += 1

        currentvalue = table[i.translated]
        currentkey = i.translated
        for key, value in table.items():
            if value > currentvalue:
                currentkey = key
                currentvalue = value
        if currentvalue > 0 and currentkey != i.translated:
            newdict = i.dict
            newdict['translated'] = currentkey
            newdict['release'] = 0
            return pygame.event.Event(i.type, newdict)
    return i

def translate(event):
    global lastaxisvalue, lasthatvalue, Cheatstring
    normalized = None
    translated = None
    all = 0
    release = 0
    if event.type in (KEYDOWN, KEYUP):
        # K_NUMLOCK and K_CAPSLOCK don't work right in pygame
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                Cheatstring = Cheatstring[:-1]
            else:
                try:
                    Cheatstring = Cheatstring[-4:]+event.unicode
                except (TypeError, AttributeError):
                    Cheatstring = ''
        if event.key == K_PRINT:
            if event.type == KEYDOWN:
                global ScreenshotNum
                dir = os.environ.get('HOME', '.')
                file = 'solarwolf%02d.bmp' % ScreenshotNum
                fullname = os.path.join(dir, file)
                print 'Screenshot:', fullname
                try:
                    pygame.image.save(pygame.display.get_surface(), fullname)
                except:
                    print ' Screenshot FAILED'
                ScreenshotNum += 1
        elif event.key not in (K_NUMLOCK, K_CAPSLOCK):
            normalized = event.key
            translated = translations[KEYDOWN].get(normalized, DEFAULT)
            if translated == DEFAULT:
                translated = translations[NOEVENT].get(KEYDOWN, None)
                all = 1
            if event.type == KEYUP:
                release = 1
    elif event.type == JOYAXISMOTION:
        value = None
        if event.value > .8:
            value = AXISMORE
        elif event.value < -.8:
            value = AXISLESS
        axis = event.axis
        if value != lastaxisvalue[axis]:
            if lastaxisvalue[axis] == None:
                lastaxisvalue[axis] = value
                if value != None:
                    normalized = axis * 2 + value
                    translated = translations[JOYAXISMOTION].get(normalized, DEFAULT)
                    if translated == DEFAULT:
                        translated = translations[NOEVENT].get(JOYAXISMOTION, None)
                        all = 1
            else:
                normalized = axis * 2 + lastaxisvalue[axis]
                translated = translations[JOYAXISMOTION].get(normalized, DEFAULT)
                if translated == DEFAULT:
                    translated = translations[NOEVENT].get(JOYAXISMOTION, None)
                    all = 1
                if value != None:
                    pygame.event.post(event)
                release = 1
                lastaxisvalue[axis] = None
    elif event.type == JOYHATMOTION:
        hat = event.hat
        value = [
            (HATLEFT, None, HATRIGHT)[-1 * event.value[0] + 1],
            (HATUP, None, HATDOWN)[-1 * event.value[1] + 1]
        ]
        for axis in (0, 1):
            if value[axis] != lasthatvalue[hat][axis]:
                if lasthatvalue[hat][axis] == None:
                    lasthatvalue[hat][axis] = value[axis]
                    if value[axis] != None:
                        normalized = hat * 4 + value[axis]
                        translated = translations[JOYHATMOTION].get(normalized, DEFAULT)
                        if translated == DEFAULT:
                            translated = translations[NOEVENT].get(JOYHATMOTION, None)
                            all = 1
                else:
                    normalized = hat * 4 + lasthatvalue[hat][axis]
                    translated = translations[JOYHATMOTION].get(normalized, DEFAULT)
                    if translated == DEFAULT:
                        translated = translations[NOEVENT].get(JOYHATMOTION, None)
                        all = 1
                    if value[axis] != None:
                        pygame.event.post(event)
                    release = 1
                    lasthatvalue[hat][axis] = None
    elif event.type in (JOYBUTTONDOWN, JOYBUTTONUP):
        normalized = event.button
        translated = translations[JOYBUTTONDOWN].get(normalized, DEFAULT)
        if translated == DEFAULT:
            translated = translations[NOEVENT].get(JOYBUTTONDOWN, None)
            all = 1
        if event.type == JOYBUTTONUP:
            release = 1
    elif event.type == FINISHMUSIC:
        snd.finish_playmusic()
    newdict = event.dict
    newdict['normalized'] = normalized
    newdict['translated'] = translated
    newdict['all'] = all
    newdict['release'] = release
    return pygame.event.Event(event.type, newdict)


def input_text(type, normalized):
    global hat_direction_text
    if type == KEYDOWN:
        # K_NUMLOCK and K_CAPSLOCK don't work in pygame
        if normalized not in (K_NUMLOCK, K_CAPSLOCK):
            return 'Key' + pygame.key.name(normalized).title().replace(' ', '')
    elif type == JOYBUTTONDOWN:
        return 'Btn' + str(normalized)
    elif type == JOYAXISMOTION:
        if normalized % 2 == 0:
            direction = "-"
            value = AXISLESS
        else:
            direction = "+"
            value = AXISMORE
        axis = str( (normalized - value) / 2 )
        return 'Axis' + axis + direction
    elif type == JOYHATMOTION:
        value = HATSTART + normalized % 4
        direction = hat_direction_text[value]
        hat = str( (normalized - value) / 4 )
        return 'Hat' + hat + direction
    elif type == NOEVENT:
        return "*AllElse*"

def getdisplay():
    global translations
    display = {}
    for type, table in translations.items():
        for normalized, action in table.items():
            if not display.has_key(action):
                display[action] = []
            if type != NOEVENT:
                display[action].append((type, normalized))
            else:
                if normalized == KEYDOWN:
                    display[action].append((type, normalized))
    for a in actions_order:
        display[a].sort()

    return display


def setdisplay(display):
    global translations
    translations.clear()
    translations[NOEVENT] = {}

    for a in actions_order:
        for l in range(len(display[a])):
            type = display[a][l][0]
            normalized = display[a][l][1]
            if not translations.has_key(type):
                translations[type] = {}
            if type != NOEVENT:
                translations[type][normalized] = a
            else:
                translations[type][KEYDOWN] = a
                translations[type][JOYBUTTONDOWN] = a

def load_translations():
    global translations
    global translations_default
    translations = {}
    #just sticking to the standard controls for now
    #try:
    #    filename = game.make_dataname('input')
    #    translations = pickle.load(open(filename, 'rb'))
    #except (IOError, OSError, KeyError):
        #print 'ERROR OPENING CONTROL FILE, loading defaults'
    if 1:
        translations = translations_default

def save_translations():
    global translations
    #not gonna save for now
    return
    try:
        filename = game.make_dataname('input')
        f = open(filename, 'wb')
        p = pickle.Pickler(f, 1)
        p.dump(translations)
        f.close()
    except (IOError, OSError), msg:
        import messagebox
        messagebox.error("Error Saving Control Data",
"There was an error saving the control data.\nCurrent player controls have been lost.\n\n%s"%msg)
