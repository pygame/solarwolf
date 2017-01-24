import objbox, game
import pygame


Levels = []
initialized = 0

def init():
    global Levels, initialized
    curlev = []
    f = game.get_resource('levels.txt')
    f = open(f, 'r')
    curtitle = curtitle2 = ''
    while 1:
        l = f.readline()
        if l and l[0] == '>':
            curtitle = l[1:].strip()
            continue
        if l and l[0] == '<':
            curtitle2 = l[1:].strip()
            continue
        if curlev and (not l or l[0] == '!'):
            for i in range(7-len(curlev)):
                curlev.append('         ')
            curlev.insert(0, curtitle2)
            curlev.insert(0, curtitle)
            Levels.append(curlev)
            curtitle = curtitle2 = ''
            curlev = []
        if not l: break
        if l[0] == '!' or l[0] == ';':
            continue
        if len(curlev) < 7:
            l = (l.rstrip() + '          ')[:9]
            curlev.append(l)
    initialized = 1


def makelevel(level):
    "returns (list, startcenter) level number"
    if not initialized: init()
    lev = Levels[level%len(Levels)]
    touches = level//len(Levels) + 1
    passes = (level>len(Levels) and 2) or 1
    boxlist = []
    size = 58, 58
    corner = 106, 106
    startpos = corner[0]+236, corner[1]+182
    pos = [corner[0], corner[1]]
    numboxes = level//2
    for row in lev[2:]:
        cells = list(row)
        if touches == 2:
            cells.reverse()
        for cell in cells:
            if cell == '#':
                boxlist.append(objbox.Box(pos, touches))
                numboxes += touches
            elif cell == '*':
                boxlist.append(objbox.Box(pos, touches+1))
                numboxes += touches + 1
            elif cell == 's':
                startpos = pos[0] , pos[1]
            pos[0] = pos[0] + size[0]
        pos[0] = corner[0]
        pos[1] = pos[1] + size[1]
    msg = ''
    msg = lev[int(touches-1)]
    if level == maxlevels()-1: msg = 'Final Level'
    return boxlist, startpos, msg, numboxes


def preview(level):
    "returns (list, startcenter) level number"
    if not initialized: init()
    lev = Levels[level%len(Levels)]
    touches = level//len(Levels) + 1
    passes = (level>len(Levels) and 2) or 1
    boxlist = []
    size = 5, 5
    corner = 5, 5
    startpos = corner[0]+236, corner[1]+182
    pos = [corner[0], corner[1]]
    numboxes = level//2
    img = pygame.Surface((52, 42))
    img.fill((20, 20, 30))
    pygame.draw.rect(img, (255, 255, 255), (0,0,51,41), 2)
    colors = (150,150,150), (60, 255, 60), (255, 255, 60), (255, 60, 60)
    for row in lev[2:]:
        cells = list(row)
        if touches == 2:
            cells.reverse()
        for cell in cells:
            if cell == '#':
                img.fill(colors[touches], (pos, (2, 2)))
            elif cell == '*':
                img.fill(colors[touches+1], (pos, (2, 2)))
            elif cell == 's':
                img.fill(colors[0], (pos, (2, 2)))
            pos[0] = pos[0] + size[0]
        pos[0] = corner[0]
        pos[1] = pos[1] + size[1]
    return img

def maxlevels():
    return len(Levels) * 2


def numrocks(level):
    if level >= maxlevels():
        return 18
    percent = float(level) // maxlevels()
    return int(percent * 12)
