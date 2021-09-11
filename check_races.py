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
from datetime import datetime

import update_json
import read_json
import send_email

import Magnet_To_Torrent2 as m2t

# vars
page = Request("https://www.ettvcentral.com/user/smcgill1969/index.html", headers={'User-Agent': 'Mozilla5/0'})
webpage = urlopen(page).read()
soup = BeautifulSoup(webpage,'html.parser')
feedData = os.path.dirname(os.path.realpath(__file__)) + "/static/config.json"
time_now = str(datetime.now())

# All the crazy lists that I have to add info to and then parse out
key_word = ["2021", "Race", "SD"]
race_types = ["Formula.1","MotoGP"]
titles = []
links = []
races = []
motogp = []
formula1 = []

'''
    class to actually scrape where the torrent is from
    the link that we read from the json file
'''

class scrape:

    def __init__(self,ettv_page):
        self.page = Request(ettv_page,headers={'User-Agent': 'Mozilla5/0'})
        self.webpage = urlopen(self.page).read()
        self.soup = BeautifulSoup(self.webpage,'html.parser')
        self.result = self.soup.find_all("a", class_="fw-bold")

        for self.download_link in self.result:
            self.torrent_text = self.download_link.text
            self.torrent_link = self.download_link.get("href")



'''
    Main function will simply scrape the page finding where the MotoGP and F1 info is for Races, 2019 and in SD
    Then we are going to grab that info and update the list in the JSON file /static/config.json
    The config.json file is used to determine if the latest race is new or not
'''

def main():

    formula1_watch = read_json.output_config()["formula1_watch_directory_base"]
    motogp_watch = read_json.output_config()["motogp_watch_directory_base"]


    for data in soup.find_all('table', class_='table table-hover table-bordered'):
        for a in data.find_all('a'):
            titles.append(a.get('title'))
            links.append(a.get('href'))

    for entries in titles:
        if(entries != None):
            if all(word in entries for word in key_word):
                    races.append(entries)
    for items in races:
            for a in soup.find_all("a",attrs={"title": re.compile(items)}):
                    torrent_link = a["href"]
                    torrent_title = a["title"]
                    #print(torrent_title)

                    if("MotoGP" in torrent_title):
                        motogp.append(torrent_title + " : " + "https://www.ettvcentral.com" + torrent_link)

                    if("Formula" in torrent_title):
                        formula1.append(torrent_title + " : " + "https://www.ettvcentral.com" + torrent_link)

    # MotoGP
    try:
        '''
        check to see if the race name and the link to the page are the same as what
        is in the json file
        If not, call the scrape class and grab the text in the link as well as the link
        Then we simply call wget to grab the torrent
        '''
        if(read_json.output_config()["motogp_title"] != str(motogp[0])):
            update_json.updateJsonFile("motogp_title",motogp[0])
            update_json.updateJsonFile("motogp_update","Yes")
            motogp_output = read_json.output_config()["motogp_title"]
            motogp_partition = (motogp_output.partition(":"))
           
            torrent_page = motogp_partition[2]
            t = scrape(torrent_page)
            
            if(t.torrent_text == "Download Torrent (File)"):
                print("Torrent found....proceed with download")
                subprocess.call(["wget",t.torrent_link,"-P",motogp_watch])

                #update the json file with information
                update_json.updateJsonFile("last_run",time_now)
                update_json.updateJsonFile("motogp_update","No")
                update_json.updateJsonFile("motogp_rtorrent_email","No")
                send_email.send_email("New MotoGP Race",motogp[0])
    except:
        update_json.updateJsonFile("last_run",time_now)
        update_json.updateJsonFile("formula1_update","No")


    # Formula 1
    try:
        if(read_json.output_config()["formula1_title"] != str(formula1[0])):
            update_json.updateJsonFile("formula1_title",formula1[0])
            update_json.updateJsonFile("formula1_update","Yes")
            formula1_output = read_json.output_config()["formula1_title"]
            formula1_partition = (formula1_output.partition(":"))
            
            t = scrape(formula1_partition[2])

            if(t.torrent_text == "Download Torrent (File)"):
                print("Torrent found....proceed with download")
                subprocess.call(["wget",t.torrent_link,"-P",formula1_watch])


                #update the json file with information
                update_json.updateJsonFile("last_run",time_now)
                update_json.updateJsonFile("formula1_update","No")
                update_json.updateJsonFile("formula1_rtorrent_email","No")
                send_email.send_email("New Formula 1 Race", formula1[0])

    except:
        update_json.updateJsonFile("last_run",time_now)
        update_json.updateJsonFile("formula1_update","No")

if __name__ == "__main__":
    print(time_now)
    main()
