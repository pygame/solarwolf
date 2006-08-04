"""audio class, helps everyone to audio"""

import pygame, os
from pygame.locals import *
import game, input


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
    prefvolume = [0, 0.6, 1.0][game.volume]
    volume *= prefvolume
    if not volume:
        return
    sound = fetch(name)
    if sound:
        chan = sound.play()
        if not chan:
            chan = pygame.mixer.find_channel(1)
            chan.play(sound)
        if chan:
            if pos == -1:
                percent = 0.5
            else:
                percent = (pos / 700.0)
            inv = 1.0 - percent
            chan.set_volume(inv*volume, percent*volume)

CurrentSong = None
CurrentVolume = 1.0
SwitchingSongs = 0
def playmusic(musicname, volume=1.0):
    if not music or not game.music: return
    global CurrentSong, SwitchingSongs, CurrentVolume
    if musicname == CurrentSong:
        return
    CurrentSong = musicname
    CurrentVolume = volume
    if SwitchingSongs:
        CurrentSong = musicname
    SwitchingSongs = 1
    if music.get_busy():
        music.set_endevent(input.FINISHMUSIC)
        music.fadeout(1000)
    else:
        prefvolume = [0, 0.6, 1.0][game.music]
        fullname = os.path.join('data', 'music', musicname)
        music.load(fullname)
        music.play(-1)
        music.set_volume(prefvolume*CurrentVolume)

def finish_playmusic():
    global CurrentSong, SwitchingSongs, CurrentVolume
    SwitchingSongs = 0
    prefvolume = [0, 0.6, 1.0][game.music]
    fullname = os.path.join('data', 'music', CurrentSong)
    music.load(fullname)
    music.play(-1)
    music.set_volume(prefvolume*CurrentVolume)



def tweakmusicvolume():
    if not music:
        return
    prefvolume = [0, 0.6, 1.0][game.music]
    if not prefvolume:
        music.stop()
    if not music.get_busy():
        music.play(-1)
    music.set_volume(prefvolume*CurrentVolume)

