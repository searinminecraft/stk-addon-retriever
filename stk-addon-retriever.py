#!/usr/bin/env python3

import os
import shutil
import sys
import xml.etree.ElementTree as elementtree
from urllib import request

try:
    from pick import pick
except ImportError:
    print('This script is useless without the dependency \'pick\'. Please install that dependency first before running this script.')
    sys.exit(1)


# "borrowed" some code from ultimate stk launcher

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

stkaddons = 'https://online.supertuxkart.net/downloads/xml/online_assets.xml'

# openrc inspired log

def log(text, level):
    # info
    if level == 0:
        print(color.BOLD + "       " + text + color.END)
    # error
    elif level == 1:
        print(color.BOLD + color.BLUE + "[" + color.RED + " !! " + color.BLUE + "]" + color.END + " " + text + color.END)
    # success
    elif level == 2:
        print(color.BOLD + color.BLUE + "[" + color.GREEN + " ok " + color.BLUE + "]" + color.END + " " + text + color.END)
    # warning
    elif level == 3:
       print(color.BOLD + color.BLUE + "[" + color.YELLOW + " !! " + color.BLUE + "]" + color.END + " " + text + color.END)

def get_addons_db():
    
    try:
        log("Retrieving addons.xml from SuperTuxKart servers.", 0)
        
        request.urlretrieve(stkaddons, os.getcwd() + '/addons.xml')
    except:
       log("Could not get addons.xml. Quitting.", 1) 
    else:
        log("Successfully retrieved addons.xml.",2)

def getaddons(choice):

    get_addons_db()

    addonsfile = elementtree.parse(os.getcwd() + '/addons.xml')
    root = addonsfile.getroot()

    if choice == 1:
        log("Downloading Karts...", 0)
        for kart in root.findall('kart'):
            url = kart.get('file')
            id = kart.get('id')
            name = kart.get('name')
            revision = kart.get('revision')

            try:
                log("Downloading Kart " + "\"" + name + "\". (Revision " + revision + ")", 0)

                request.urlretrieve(url, os.getcwd() + '/' + id + '.zip')

                if os.name == 'posix': # linux
                    shutil.unpack_archive(os.getcwd() + '/' + id + '.zip', '/home/' + os.environ.get('USER') + '/.local/share/supertuxkart/addons/karts/' + id)
                    os.system('rm ' + os.getcwd() + '/' + id + '.zip')
                else: # windows
                    shutil.unpack_archive(os.getcwd() + '\\' + id + '.zip', 'C:\\Users\\' + os.environ.get('USERNAME') + '\\AppData\\Roaming\\supertuxkart\\addons\\karts\\' + id)
                    os.system('del ' + os.getcwd() + '\\' + id + '.zip')

            except:
                log("Failed to download " + "\"" + name + "\" (Revision " + revision + ")", 1)
            else:
                log("Succssfully downloaded " + "\"" + name + "\"", 2)

    elif choice == 2:
        log("Downloading Tracks...", 0)
        for track in root.findall('track'):
            url = track.get('file')
            id = track.get('id')
            name = track.get('name')
            revision = track.get('revision')

            try:
                log("Downloading Track " + "\"" + name + "\". (Revision " + revision + ")", 0)

                request.urlretrieve(url, os.getcwd() + '/' + id + '.zip')

                if os.name == 'posix': # linux
                    shutil.unpack_archive(os.getcwd() + '/home/' + os.environ.get('USER') + '/.local/share/supertuxkart/addons/tracks/' + id)
                    os.system('rm ' + os.getcwd() + '/' + id + '.zip')
                else: # windows
                    shutil.unpack_archive(os.getcwd() + '\\' + id + '.zip', 'C:\\Users\\' + os.environ.get('USERNAME') + '\\AppData\\Roaming\\supertuxkart\\addons\\tracks\\' + id)
                    os.system('del ' + os.getcwd() + '\\' + id + '.zip')

            except:
                log("Failed to download " + "\"" + name + "\" (Revision " + revision + ")", 1)
            else:
                log("Succssfully downloaded " + "\"" + name + "\"", 2)

    elif choice == 3:
        log("Downloading Arenas...", 0)
        for arena in root.findall('arena'):
            url = arena.get('file')
            id = arena.get('id')
            name = arena.get('name')
            revision = arena.get('revision')

            try:
                log("Downloading Arena " + "\"" + name + "\". (Revision " + revision + ")", 0)

                request.urlretrieve(url, os.getcwd() + '/' + id + '.zip')

                if os.name == 'posix': # linux
                    shutil.unpack_archive(os.getcwd() + '/home/' + os.environ.get('USER') + '/.local/share/supertuxkart/addons/tracks/' + id)
                    os.system('rm ' + os.getcwd() + '/' + id + '.zip')
                else: # windows
                    shutil.unpack_archive(os.getcwd() + '\\' + id + '.zip', 'C:\\Users\\' + os.environ.get('USERNAME') + '\\AppData\\Roaming\\supertuxkart\\addons\\tracks\\' + id)
                    os.system('del ' + os.getcwd() + '\\' + id + '.zip')

            except:
                log("Failed to download " + "\"" + name + "\" (Revision " + revision + ")", 1)
            else:
                log("Succssfully downloaded " + "\"" + name + "\"", 2)

def main():
    
    os.system('cls' if os.name == 'nt' else 'clear')

    choicename = 'What do you want to do?'
    choices = ['Install EVERYTHING', 'Install Karts', 'Install Tracks', 'Install Arenas', 'List Addons', 'Exit']

    option, index = pick(choices, choicename)

    print('')

    if index == 0:
        choicename = 'Warning: This will take a VERY VERY long time. Are you sure you want to do this?'
        choices = ['Yeah', 'Nope!']

        option, index = pick(choices, choicename)

        if index == 0:
            log("Beginning to download ALL addons.", 3)
            getaddons(1)
            getaddons(2)
            getaddons(3)
        else:
            main()

    elif index == 1:
        getaddons(1)
    elif index == 2:
        getaddons(2)
    elif index == 3:
        getaddons(3)
    elif index == 4:
        print('Function not implemented, yet.')
        input("Press Enter to continue.")
        main()
    elif index == 5:
        print('Bye bye!')

if __name__ == '__main__':
    main()
