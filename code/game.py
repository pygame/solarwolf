"""game module, place for global game state"""

import os
from pygame.rect import Rect
from cStringIO import StringIO




#various data constants
start_lives = 3

ship_fastspeed = 7
ship_slowspeed = 5
shot_speed = 3

guard_speed = 4
guard_fire = .01
fire_factor = .15


arena = Rect(55, 50, 590, 490)

poweruptime = 1200.0
powerupspeed = 2.0
powerupwait = 26.0 #45.0
asteroidspeed = 1.4

timeleft = 0.0
timetick = 0.0
timefactor = 12.2    #how quickly time drops (bigger = slower)
speedmult = 0

musictime = 1000 * 120 #two minutes

text_length = 80  #frames text is displayed in-game


site_url = 'http://pygame.org/shredwheat/solarwolf'
news_url = 'http://pygame.org/shredwheat/solarwolf/thenews.html'



#number of insults must match num of complements, be careful
Complements = (
    'Keep it up!',
    'Looking Great!',
    'Hotshot',
    'Too Hot to Handle',
    'Bring it on',
    'Beautiful',
    'Own the Zone',
    'Too Cool For School',
    'So Hot Right Now',
    'Smooth Moves'
)
Insults = (
    'Not so good',
    'Ouch',
    'Rookie',
    'Sloppy',
    'Choke Choke',
    'Not Today',
    'Hall of Shame',
    'Wrong way',
    'Clumsy, Clumsy',
    'Medic',
)



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



#these are the defualt 'setup' controlled by Preferences
music = 2
volume = 2
display = 1
help = 0
thruster = 0
comments = 1


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

version = "1.5"
DEBUG = 0
