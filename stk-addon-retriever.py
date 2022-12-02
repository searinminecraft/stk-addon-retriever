#!/usr/bin/env python3

import os
import shutil
import sys
import xml.etree.ElementTree as elementtree

try:
    from pick import pick
    import requests
except ImportError:
    print('Some dependencies are missing. Please install the mentioned dependencies from the README to continue.')
    sys.exit(1)



version = '1.3'

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

headers = {'user-agent': 'Mozilla/5.0 (compatible; STKAddonRetriever/' + version + '; https://github.com/searinminecraft/stk-addon-retrievrer'}

# openrc inspired log

def log(text: str, level: int):
    # info
    if level == 0:
        print("       " + text + color.END)
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
        
        content = requests.get(stkaddons, headers=headers)

        with open('addons.xml', 'wb') as file:
            file.write(content.content)
    except requests.exceptions.ConnectionError as e:
       log("Could not retrieve addons.xml: Can't connect to " + stkaddons + ".\n\nDetailed information:\n\nException: " + str(type(e)) + "\n\nMessage: "  + str(e) + "\n", 1)
       sys.exit(1)
    except Exception as e:
        log("An error occured while retrieving addons.xml.\n\nDetailed information:\n\nException: " + str(type(e)) + "\n\nMessage: " + str(e), 1)
        sys.exit("1")
    except KeyboardInterrupt:
        log("Interrupt signal recieved.", 1)
        sys.exit(1)
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

                try:
                    if os.name == 'posix':
                        os.chdir(os.path.expanduser('~') + '/.local/share/supertuxkart/addons/karts/' + id)
                    else:
                        os.chdir('C:\\Users\\' + os.environ.get('USERNAME') + '\\AppData\\Roaming\\supertuxkart\\addons\\karts')
                
                    ident = elementtree.parse('kart.xml')
                    ver = ident.getroot().get('revision')

                    if int(ver) >= int(revision):
                        raise TypeError(id + ' already exists or already in latest version!!' + ' Current Revision: ' + ver + ', New Revision: ' + revision)
                
                except FileNotFoundError:
                    pass

                content = requests.get(url , headers=headers)

                with open(id+'.zip', 'wb') as file:
                    file.write(content.content)

                if os.name == 'posix': # linux
                    shutil.unpack_archive(os.getcwd() + '/' + id + '.zip', os.path.expanduser('~') + '/.local/share/supertuxkart/addons/karts/' + id)
                    os.remove(id + '.zip')
                else: # windows
                    shutil.unpack_archive(os.getcwd() + '\\' + id + '.zip', 'C:\\Users\\' + os.environ.get('USERNAME') + '\\AppData\\Roaming\\supertuxkart\\addons\\karts\\' + id)
                    os.remove(id + '.zip')

            except requests.exceptions.ConnectionError as e:
                log("Failed to download " + "\"" + name + "\" (Revision " + revision + "): " + str(e), 1)
            except KeyboardInterrupt:
                log("Interrupt signal recieved.", 1)
                sys.exit(1)
            except TypeError as e:
                log(str(e), 1)
            except Exception as e:
                log("An unexpected error has occured: " + str(e), 1)
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

                try:
                    if os.name == 'posix':
                        os.chdir(os.path.expanduser('~') + '/.local/share/supertuxkart/addons/tracks/' + id)
                    else:
                        os.chdir('C:\\Users\\' + os.environ.get('USERNAME') + '\\AppData\\Roaming\\supertuxkart\\addons\\tracks')
                
                    ident = elementtree.parse('track.xml')
                    ver = ident.getroot().get('revision')

                    if int(ver) >= int(revision):
                        raise TypeError(id + ' already exists or already in latest version!!' + ' Current Revision: ' + ver + ', New Revision: ' + revision)
                
                except FileNotFoundError:
                    pass

                content = requests.get(url , headers=headers)

                with open(id+'.zip', 'wb') as file:
                    file.write(content.content)

                if os.name == 'posix': # linux
                    shutil.unpack_archive(os.getcwd() + '/' + id + '.zip', os.path.expanduser('~') + '/.local/share/supertuxkart/addons/tracks/' + id)
                    os.remove(id + '.zip')
                else: # windows
                    shutil.unpack_archive(os.getcwd() + '\\' + id + '.zip', 'C:\\Users\\' + os.environ.get('USERNAME') + '\\AppData\\Roaming\\supertuxkart\\addons\\tracks\\' + id)
                    os.remove(id + '.zip')

            except requests.exceptions.ConnectionError as e:
                log("Failed to download " + "\"" + name + "\" (Revision " + revision + "): " + str(e), 1)
            except KeyboardInterrupt:
                log("Interrupt signal recieved.", 1)
                sys.exit(1)
            except TypeError as e:
                log(str(e), 1)
            except Exception as e:
                log("An unexpected error has occured: " + str(e), 1)
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

                try:
                    if os.name == 'posix':
                        os.chdir(os.path.expanduser('~') + '/.local/share/supertuxkart/addons/tracks/' + id)
                    else:
                        os.chdir('C:\\Users\\' + os.environ.get('USERNAME') + '\\AppData\\Roaming\\supertuxkart\\addons\\tracks')
                
                    ident = elementtree.parse('track.xml')
                    ver = ident.getroot().get('revision')

                    if int(ver) >= int(revision):
                        raise TypeError(id + ' already exists or already in latest version!!' + ' Current Revision: ' + ver + ', New Revision: ' + revision)
                
                except FileNotFoundError:
                    pass

                content = requests.get(url , headers=headers)

                with open(id+'.zip', 'wb') as file:
                    file.write(content.content)

                if os.name == 'posix': # linux
                    shutil.unpack_archive(os.getcwd() + '/' + id + '.zip', os.path.expanduser('~') + '/.local/share/supertuxkart/addons/tracks/' + id)
                    os.remove(id + '.zip')
                else: # windows
                    shutil.unpack_archive(os.getcwd() + '\\' + id + '.zip', 'C:\\Users\\' + os.environ.get('USERNAME') + '\\AppData\\Roaming\\supertuxkart\\addons\\tracks\\' + id)
                    os.remove(id + '.zip')

            except requests.exceptions.ConnectionError as e:
                log("Failed to download " + "\"" + name + "\" (Revision " + revision + "): " + str(e), 1)
            except KeyboardInterrupt:
                log("Interrupt signal recieved.", 1)
                sys.exit(1)
            except TypeError as e:
                log(str(e), 1)
            except Exception as e:
                log("An unexpected error has occured: " + str(e), 1)
            else:
                log("Succssfully downloaded " + "\"" + name + "\"", 2)

def main():
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    choicename = 'What do you want to do today?'
    choices = ['Install/Update EVERYTHING', 'Install/Update Karts', 'Install/Update Tracks', 'Install/Update Arenas', 'List Addons', 'Exit']

    option, index = pick(choices, choicename)

    if index == 0:
        choicename = 'Warning: This will take a VERY VERY long time (depending on your internet connection). Are you sure you want to do this?'
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
        sys.exit(0)

if __name__ == '__main__':
    try:
        import setproctitle
        setproctitle.setproctitle('STK Addon Retiever ' + version)
    except ImportError:
        pass

    main()
