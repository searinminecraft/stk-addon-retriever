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
        print(value + " " + name)

def main():
    get_addons()
    parse_addons()

if __name__ == '__main__':
    main()