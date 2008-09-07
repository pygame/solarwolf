# solarwolf - collecting and dodging arcade game
# Copyright (C) 2006  Pete Shinners <pete@shinners.org>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

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



