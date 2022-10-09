import os
import sys
import requests
import xml.etree.ElementTree as elementtree

from pick import pick

stkdir = '$HOME/.local/share/supertuxkart/addons'
kartsdir = stkdir + '/karts'
tracksdir = stkdir + '/tracks'

def get_addons():
    
    try:
        print('Please wait while I get addons.xml')
        content = requests.get('https://online.supertuxkart.net/downloads/xml/online_assets.xml')
    except:
        print("Failed to download addon data! Quitting...")
        sys.exit(1)

    with open('addons.xml', 'wb') as f:
        f.write(content.content)

def downloadall(choice):

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
                os.system('curl -fsSL ' + value + ' -o /tmp/test.zip && unzip -o /tmp/test.zip -d ' + kartsdir + '/' + id + ' && rm /tmp/test.zip')
            except:
                print("ERROR: Failed to download/extract " + name + ".")


    elif choice == 2:

        print('Downloading Tracks...')
        for item in root.findall('track'):
            value = item.get('file')
            id = item.get('id')
            name = item.get('name')
            revision = item.get('revision')
            print("Track: " + name + ", URL: " + value + ", Revision: " + revision)

            try:
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
    
    get_addons()

    choicename = 'What do you want to do?'
    choices = ['Install EVERYTHING', 'Install Karts', 'Install Tracks', 'Install Arenas', 'Just get all information and exit.', 'Exit']

    option, index = pick(choices, choicename)

    print('')

    if index == 0:
        choicename = 'This will take a VERY VERY long time. Are you sure you want to do this?'
        choices = ['Yeah', 'Nope!']
        
        option, index = pick(choices, choicename)

        if index == 0:
            downloadall(1)
            downloadall(2)
            downloadall(3)
        else:
            print('Exiting...')

    elif index == 1:
        downloadall(1)
    elif index == 2:
        downloadall(2)
    elif index == 3:
        downloadall(3)
    elif index == 4:
        print('Function not implemented, yet.')
    elif index == 5:
        print('Bye bye!')
    
if __name__ == '__main__':
    main()