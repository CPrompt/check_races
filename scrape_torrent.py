#!/usr/bin/python3

'''
This will read the config file (config.json)
See if any of the race entries are set to "Yes"
If so, read the torrent link and start the scraping
Download the torrent and move it to the directory for rtorrent to pickup
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


# function to take the link that is passed, scrape it and then return the link to the torrent
def scrape_page(page):
    global torrent_file

    page = Request(page,headers={'User-Agent': 'Mozilla5/0'})
    webpage = urlopen(page).read()
    soup = BeautifulSoup(webpage,'html.parser')
    for a in soup.find_all("a", {"class":"download_link file"}):
        torrent_file = a['href']
        return(torrent_file)



# we have a new race
# go to the page in the config file
# start the scrapping!
def grab_torrent():

    if(settings.f1torrent_status == "Yes"):
        print("New F1 Race: " + settings.formula1_title)
        scrape_page(settings.f1torrent_page)
        subprocess.call(["wget",torrent_file,"-P",settings.formula1_watch])
    else:
        print("Not Hotdog")

    if(settings.motogp_status == "Yes"):
        print("New MotoGP Race: " + settings.motogp_title)
        scrape_page(settings.motogp_page)
        print(torrent_file)
        subprocess.call(["wget",torrent_file,"-P",settings.motogp_watch])
    else:
        print("Not Hotdog")


if __name__ == "__main__":
    grab_torrent()
