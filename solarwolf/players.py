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

#player data... wooo


#each player needs a name, guid, score
#high score list has name, guid, score

import random, sys, game, pickle

players = []
winners = []


def new_guid():
    return str(random.randint(0, sys.maxint-1))

def make_winner(player):
    player.winner = 1
    players.remove(player)
    winners.insert(0, player)
    game.player = None

class Player:
    def __init__(self, name, guid=None, score=0):
        self.name = name
        self.score = score
        self.skips = 0
        self.winner = 0
        self.lives = 0
        self.cheater = 0
        self.help = {}
        if guid:
            self.guid = guid
        else:
            self.newguid()

    def __str__(self):
        vals = self.name, self.guid, self.score
        return 'Player(%s, %s, %d)' % vals

    def newguid(self):
        self.guid = self.name + '_' + new_guid()

    def start_level(self):
        if not self or self.score < 1:
            return 0
        return self.score

def find_player(guid):
    for p in players:
        if p.guid == guid:
            return p
    return None


def load_players():
    global players, winners
    allplayers = []
    players = []
    winners = []
    try:
        filename = game.make_dataname('players')
        allplayers = pickle.load(open(filename, 'rb'))
        for p in allplayers:
            if p.winner:
                winners.append(p)
                if not hasattr(p, "lives"):
                    p.lives = 0
                if not hasattr(p, "skips"):
                    p.skips = 0
                if not hasattr(p, "cheater"):
                    p.cheater = 0
            else:
                players.append(p)
                if not hasattr(p, "help"):
                    p.help = {}
                if not hasattr(p, "lives"):
                    p.lives = p.score * 2
                if not hasattr(p, "skips"):
                    p.skips = 0
                if not hasattr(p, "cheater"):
                    p.cheater = 0
    except (IOError, OSError, KeyError, IndexError):
        players = []
        #print 'ERROR OPENING PLAYER FILE'



def save_players():
    allplayers = players + winners
    try:
        filename = game.make_dataname('players')
        f = open(filename, 'wb')
        p = pickle.Pickler(f, 1)
        p.dump(allplayers)
        f.close()
    except (IOError, OSError), msg:
        import errorbox
        errorbox.errorbox("Error Saving Player Data",
"There was an error saving the player data.\nCurrent player data has been lost.\n\n%s"%msg)
