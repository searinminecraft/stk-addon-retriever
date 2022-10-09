import os
import sys
import requests
import xml.etree.ElementTree as elementtree

def get_addons():

    try:
        content = requests.get('https://online.supertuxkart.net/downloads/xml/online_assets.xml')
    except:
        print("Failed to download addons!!")
        sys.exit(1)

    with open('addons.xml', 'wb') as f:
        f.write(content.content)

def parse_addons():

    element = elementtree.parse('addons.xml')
    root = element.getroot()

    for item in root.findall('kart'):
        value = item.get('file')
        name = item.get('name')
        revision = item.get('revision')
        print("Kart: " + name + " URL: " + value + " Revision: " + revision)
    
    for item in root.findall('track'):
        value = item.get('file')
        name = item.get('name')
        revision = item.get('revision')
        print("Track: " + name + " URL: " + value + " Revision: " + revision)

    for item in root.findall('arena'):
        value = item.get('file')
        name = item.get('name')
        revision = item.get('revision')
        print("Arena: " + name + " URL: " + value + " Revision: " + revision)

def main():
    get_addons()
    parse_addons()

if __name__ == '__main__':
    main()