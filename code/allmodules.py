#all modules
#this is simply to ensure init type functions
#will work, because all needed game modules will
#be imported. groove on


#we'll just parse this string out and import everything in it
modules_string = """
game, gameplay, gamemenu, gamename, gamestart, gamesetup, gamewin,
gamehelp, gamepause, gamepref,
gfx, snd, txt, hud, levels, main, input, score,
objbox, objexplode, objguard, objpopshot, objtele,
objship, objshot, objsmoke, objtext, objwarp, stars, objpowerup, objasteroid
"""

def modules_import():
    mods = modules_string.split(',')
    for m in mods:
        m = m.strip()
        __import__(m)

modules_import()



