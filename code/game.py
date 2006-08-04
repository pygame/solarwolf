"""game module, place for global game state"""

import os
from pygame.rect import Rect
from cStringIO import StringIO


version = "1.0"


#various data constants
start_lives = 3

ship_fastspeed = 10
ship_slowspeed = 6

guard_speed = 5
guard_fire = .01


shot_speed = 4

arena = Rect(55, 50, 590, 490)

timeleft = 0.0
timetick = 0.0
timefactor = 14    #how quickly time drops (bigger = slower)

text_length = 80  #frames text is displayed in-game


news_url = 'http://shredwheat.zopesite.com/solarwolf/thenews'


player = None
name_maxlength = 10     #longest name

max_players = 5         #most player accounts available




#current gamehandler class instance
#this should be set by function creating new handler
handler = None



#FpsClock class, set in main.py
fpsclock = None




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
    filename = os.path.abspath(filename)
    filename = os.path.normpath(filename)
    return filename
