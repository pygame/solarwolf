"""game module, place for global game state"""

import os
from pygame.rect import Rect
from cStringIO import StringIO




#various data constants
start_lives = 3

ship_fastspeed = 8
ship_slowspeed = 5

guard_speed = 4
guard_fire = .01


shot_speed = 3

arena = Rect(55, 50, 590, 490)

timeleft = 0.0
timetick = 0.0
timefactor = 15    #how quickly time drops (bigger = slower)

text_length = 80  #frames text is displayed in-game


news_url = 'http://pygame.org/shredwheat/solarwolf/thenews.html'


player = None
name_maxlength = 10     #longest name

max_players = 5         #most player accounts available

#clock info
clock = None
clockticks = 1


#current gamehandler class instance
#this should be set by function creating new handler
handler = None
thread = None  #any background thread
stopthread = 0 #request thread terminate



def get_resource(filename):
    fullname = os.path.join('data', filename)
    return fullname


def make_dataname(filename):
    if os.name == 'posix':
        home = os.environ['HOME']
        fullhome = os.path.join(home, '.solarwolf')
        if not os.path.isdir(fullhome):
            try: os.mkdir(fullhome, 0755)
            except OSError: fullhome = home
        filename = os.path.join(fullhome, filename)
    else:
        filename = get_resource(filename)
    filename = os.path.abspath(filename)
    filename = os.path.normpath(filename)
    return filename

version = "1.1"
DEBUG = 0
