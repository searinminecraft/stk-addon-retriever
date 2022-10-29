import os
import sys
import requests
import xml.etree.ElementTree as elementtree

try:
    from pick import pick
except ImportError:
    print('This script is useless without the dependency \'pick\'. Please install that dependency first before running this script.')
    sys.exit(1)

stkdir = '$HOME/.local/share/supertuxkart/addons'
kartsdir = stkdir + '/karts'
tracksdir = stkdir + '/tracks'


def get_addons_db():

    try:
        print('Please wait while I get addons.xml')
        content = requests.get('https://online.supertuxkart.net/downloads/xml/online_assets.xml')
    except:
        print("Failed to download addon data! Quitting...")
        sys.exit(1)

    with open('addons.xml', 'wb') as f:
        f.write(content.content)

def getaddons(choice):

    get_addons_db()

    element = elementtree.parse('addons.xml')
    root = element.getroot()

    if choice == 1:
        print('Downloading Karts...')
        for item in root.findall('kart'):
            value = item.get('file')
            id = item.get('id')
            name = item.get('name')
            revision = item.get('revision')
            print("Kart: " + name + ", URL: " + value + ", Revision: " + revision)

            try:
                os.system('curl -fsSL ' + value + ' -o /tmp/test.zip  && unzip -o /tmp/test.zip -d ' + kartsdir + '/' + id + ' && rm /tmp/test.zip')
            except:
                print("ERROR: Failed to download/extract " + name + ".")


    elif choice == 2:

        print('Downloading Tracks...')
        for item in root.findall('track'):
            value = item.get('file')
            id = item.get('id')
            name = item.get('name')
            revision = item.get('revision')

            try:
                print("Downloading Track: " + name + ", URL: " + value + ", Revision: " + revision)
                os.system('curl -fsSL ' + value + ' -o /tmp/test.zip && unzip -o /tmp/test.zip -d ' + tracksdir + '/' + id + ' && rm /tmp/test.zip')
            except:
                print("ERROR: Failed to download/extract " + name + ".")

    elif choice == 3:

        print('Downloading Arenas...')
        for item in root.findall('arena'):
            value = item.get('file')
            id = item.get('id')
            name = item.get('name')
            revision = item.get('revision')
            print("Arena: " + name + ", URL: " + value + ", Revision: " + revision)

            try:
                os.system('curl -fsSL ' + value + ' -o /tmp/test.zip && unzip -o /tmp/test.zip -d ' + tracksdir + '/' + id + ' && rm /tmp/test.zip')
            except:
                print("ERROR: Failed to download/extract " + name + ".")

def main():

    if os.name == 'nt':
        print('Windows is not supported yet.')
        sys.exit(1)
    
    os.system('cls' if os.name == 'nt' else 'clear')

    choicename = 'What do you want to do?'
    choices = ['Install EVERYTHING', 'Install Karts', 'Install Tracks', 'Install Arenas', 'List Addons', 'Exit']

    option, index = pick(choices, choicename)

    print('')

    if index == 0:
        choicename = 'This will take a VERY VERY long time. Are you sure you want to do this?'
        choices = ['Yeah', 'Nope!']

        option, index = pick(choices, choicename)

        if index == 0:
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
        main()
    elif index == 5:
        print('Bye bye!')

if __name__ == '__main__':
    main()
