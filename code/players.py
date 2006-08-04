#player data... wooo


#each player needs a name, guid, score
#high score list has name, guid, score

import time, random, sys, game, pickle, tempfile
import os

players = []
winners = []


def new_guid():
    return str(random.randint(0, sys.maxint-1))

def make_winner(player):
    player.winner = 1
    players.remove(player)
    winners.insert(0, player)

class Player:
    def __init__(self, name, guid=None, score=0):
        self.name = name
        self.score = score
        self.winner = 0
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
            else:
                players.append(p)
    except (IOError, OSError, KeyError):
        players = []
        print 'ERROR OPENING PLAYER FILE'



def save_players():
    allplayers = players + winners
    try:
        filename = game.make_dataname('players')
        f = open(filename, 'wb')
        p = pickle.Pickler(f, 1)
        p.dump(allplayers)
        f.close()
    except (IOError, OSError), msg:
        import messagebox
        messagebox.error("Error Saving Player Data",
"There was an error saving the player data.\nCurrent player data has been lost.\n\n%s"%msg)
