"""audio class, helps everyone to audio"""

import pygame, os
from pygame.locals import *
import game


mixer = music = None
sound_cache = {}


def initialize():
    global mixer, music
    try:
        import pygame.mixer as pymix
        pymix.init(22000, 8, 0)
        mixer = pymix
        music = pymix.music
        return 1
    except (ImportError, pygame.error):
        return 0


def preload(*names):
    "loads a sound into the cache"
    if not mixer:
        for name in names:
            sound_cache[name] = None
        return
    for name in names:
        if not sound_cache.has_key(name):
            fullname = os.path.join('data', 'audio', name+'.wav')
            #file = game.get_resource(name+'.wav')
            try: sound = mixer.Sound(fullname)
            except: sound = None
            sound_cache[name] = sound


def fetch(name):
    if not sound_cache.has_key(name):
        preload(name)
    return sound_cache[name]



def play(name, volume=1.0, pos=-1):
    volume *= 0.5
    sound = fetch(name)
    if sound:
        chan = sound.play()
        if not chan:
            chan = pygame.mixer.find_channel(1)
            chan.play(sound)
        if chan:
            if pos == -1:
                chan.set_volume(volume)
            else:
                percent = (pos / 700.0) 
                inv = 1.0 - percent
                chan.set_volume(inv*volume, percent*volume)
    

def playmusic(musicname):
    if not music: return
    if music.get_busy():
        #we really should fade out nicely and
        #wait for the end music event, for now, CUT 
        music.stop()
    fullname = os.path.join('data', 'music', musicname)
    music.load(fullname)
    music.play(-1)
    music.set_volume(1.0)

    
