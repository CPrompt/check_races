#!/usr/bin/python3

'''
This script is to work on extracting the link from a site.
In particular this site (ettv) will have a link to the
actual torrent.

This will look for the link in the page to the torrent that is another page on ettv.tv

Next will be to use wget to download the torrent and save it to the particular directory
setup for rtorrent to watch.

'''
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, urlretrieve
import requests
import re
import os
import subprocess
import glob
import shutil
import json

import settings

# vars
webpage = urlopen(settings.page).read()
soup = BeautifulSoup(webpage,'html.parser')


# All the crazy lists that I have to add info to and then parse out
key_word = ["2019", "Race", "SD"]
race_types = ["Formula.1","MotoGP"]
titles = []
links = []
races = []
motogp = []
formula1 = []
myList = []
race_links = []
race_titles = []

'''
    Main function will simply scrape the page finding where the MotoGP and F1 info is for Races, 2019 and in SD
    Then we are going to grab that info and update the list in the JSON file /static/config.json
    The config.json file is used to determine if the latest race is new or not
'''
def main():
    '''
        look for the table with the links
        grab the title and the href for the link itself
        the title, will be used to determine what the race is
    '''
    for data in soup.find_all('table', class_='table table-hover table-bordered'):
        for a in data.find_all('a'):
            titles.append(a.get('title'))
            links.append(a.get('href'))
    '''
        Now that we have all the links, determine which ones
        match our criteria in key_word list
        For this, we only want the SD Races of 2019
    '''
    for entries in titles:
        if(entries != None):
            if all(word in entries for word in key_word):
                    races.append(entries)
    '''
        Now we need to compile seperate the links based on the titles
        if the race contains "MotoGP", add the info to the "MotoGP" list
        likewise for the formula1 races

        once we seperate them, add them to the appropriate field in the JSON file
        "static/config.json"
    '''
    for items in races:
            for a in soup.find_all("a",attrs={"title": re.compile(items)}):
                    torrent_link = a["href"]
                    torrent_title = a["title"]

                    if("MotoGP" in torrent_title):
                            motogp.append(torrent_title + " : " + "https://ettv.tv" + torrent_link)
                            settings.json_object.update_json("motogp_list",motogp)
                            print("Grabbing info from site and updating MotoGP list")

                    else:
                            formula1.append(torrent_title + " : " + "https://ettv.tv" + torrent_link)
                            settings.json_object.update_json("f1_list",formula1)
                            print("Grabbing info from site and updating Formula1 list")



if __name__ == "__main__":
    main()
