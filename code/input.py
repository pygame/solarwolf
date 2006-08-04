"translate pygame events to controls"

import pygame.joystick
from pygame.locals import *


# control constants
UP        = 1
DOWN      = 2
LEFT      = 3
RIGHT     = 4
PRESS     = 5
RELEASE   = 6
ABORT     = 7


#translation tables
keyboard_table = {
    K_UP: UP,
    K_DOWN: DOWN,
    K_LEFT: LEFT,
    K_RIGHT: RIGHT,
    K_SPACE: PRESS,
    K_RETURN: PRESS,
    K_ESCAPE: ABORT
}


joystick = None
lastjoyx = RELEASE
lastjoyy = RELEASE


def init():
    "init the joystick"
    global joystick
    try:
        num = pygame.joystick.get_count()
        if num > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
    except pygame.error:
        joystick = None


def joyindex(val):
    return int(val*1.9)+1

def translate(event):
    global lastjoyx, lastjoyy
    if event.type == KEYDOWN:
        return keyboard_table.get(event.key, None)
    elif event.type == KEYUP and event.key in (K_SPACE, K_RETURN):
        return RELEASE

    elif event.type == JOYAXISMOTION:
        if event.axis == 1:
            joy = (UP,RELEASE,DOWN)[joyindex(event.value)]
            if joy != lastjoyy:
                lastjoyy = joy
                if joy == RELEASE:
                    joy = (LEFT, RELEASE, RIGHT)[joyindex(joystick.get_axis(0))]
                    lastjoyx = joy
                if joy != RELEASE:
                    return joy
        elif event.axis == 0:
            joy = (LEFT,RELEASE,RIGHT)[joyindex(event.value)]
            if joy != lastjoyx:
                lastjoyx = joy
                if joy == RELEASE:
                    joy = (UP, RELEASE, DOWN)[joyindex(joystick.get_axis(1))]
                    lastjoyy = joy
                if joy != RELEASE:
                    return joy

    elif event.type == JOYBUTTONDOWN:
        if event.button == 0:
            return PRESS
        elif event.button > 2:
            return ABORT

    elif event.type == JOYBUTTONUP and event.button == 0:
        return RELEASE

