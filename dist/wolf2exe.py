#make standalone, needs at least pygame-1.5.3 and py2exe-0.3.1

from distutils.core import setup
import sys, os, pygame, shutil
import py2exe

#setup the project variables here.
#i can't claim these will cover all the cases
#you need, but they seem to work for all my
#projects, just change as neeeded.


script = "solarwolf.py"            #name of starting .PY
icon_file = "box.ico"                  #ICO file for the .EXE (not working well)
optimize = 0                    #0, 1, or 2; like -O and -OO
dos_console = 0                 #set to 0 for no dos shell when run
extra_data = ['data', 'readme.txt', 'lgpl.txt', 'code', 'SolarWolf Website.url'] #extra files/dirs copied to game
extra_modules = ['pygame.locals', 'random', 'math', 'threading', 'pickle', 'urllib', 'shutil']   #extra python modules not auto found






#use the default pygame icon, if none given
if not icon_file:
    path = os.path.split(pygame.__file__)[0]
    icon_file = '"' + os.path.join(path, 'pygame.ico') + '"'
#unfortunately, this cool icon stuff doesn't work in current py2exe :(
#icon_file = ''


#create the proper commandline args
args = ['py2exe', '--force', '-O'+`optimize`]
args.append(dos_console and '--console' or '--windows')
if icon_file:
    args.append('--icon')
    args.append(icon_file)
args.append('--force-imports')
args.append(','.join(extra_modules))
#args.append(','.join(pygame_modules + extra_modules))
sys.argv[1:] = args + sys.argv[1:]

project_name = os.path.splitext(os.path.split(script)[1])[0]


#this will create the executable and all dependencies
setup(name=project_name, scripts=[script])

#also need to hand copy the extra files here
def installfile(name):
    dst = os.path.join('dist', project_name)
    print 'copying', name, '->', dst
    if os.path.isdir(name):
        dst = os.path.join(dst, name)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(name, dst)
    elif os.path.isfile(name):
        shutil.copy(name, dst)
    else:
        print 'Warning, %s not found' % name




pygamedir = os.path.split(pygame.base.__file__)[0]
installfile(os.path.join(pygamedir, pygame.font.get_default_font()))
installfile(os.path.join(pygamedir, 'pygame_icon.bmp'))
for data in extra_data:
    installfile(data)