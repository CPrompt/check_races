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
import json

import update_json
import read_json
import send_email

import Magnet_To_Torrent2 as m2t

# vars
page = Request("https://www.ettv.tv/user/smcgill1969/index.html", headers={'User-Agent': 'Mozilla5/0'})
webpage = urlopen(page).read()
soup = BeautifulSoup(webpage,'html.parser')
feedData = os.path.dirname(os.path.realpath(__file__)) + "/static/config.json"


# All the crazy lists that I have to add info to and then parse out
key_word = ["2019", "Race", "SD"]
race_types = ["Formula.1","MotoGP"]
titles = []
links = []
races = []
motogp = []
formula1 = []


'''
    function to actually scrape where the torrent is from
    the link that we read from the json file
'''
class scrape:

    def __init__(self,ettv_page):
        self.page = Request(ettv_page,headers={'User-Agent': 'Mozilla5/0'})
        self.webpage = urlopen(self.page).read()
        self.soup = BeautifulSoup(self.webpage,'html.parser')
        self.result = self.soup.find_all("a", class_="download_link")

        for self.a in self.result:
            self.torrent_title = self.a["class"]
            self.torrent_file = self.a["href"]


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

                    if("MotoGP" in torrent_title):
                        motogp.append(torrent_title + " : " + "https://ettv.tv" + torrent_link)

                    if("Formula" in torrent_title):
                        formula1.append(torrent_title + " : " + "https://ettv.tv" + torrent_link)

    # MotoGP
    try:
        if(read_json.output_config()["motogp_title"] != str(motogp[0])):
            update_json.updateJsonFile("motogp_title",motogp[0])
            update_json.updateJsonFile("motogp_update","Yes")
            motogp_output = read_json.output_config()["motogp_title"]
            motogp_partition = (motogp_output.partition(":"))

            t = scrape(motogp_partition[2])
            t_title = t.torrent_title
            t_file = t.torrent_file

            # check if there is a file or just a magnet
            if(t_title[1] == "file"):
                # here we can proceed with the wget method since we have
                # an actual torrent file
                print("Processing a torrent file...")
                subprocess.call(["wget",t_file,"-P",motogp_watch])

            else:
                # here we need to run a different process
                # we can use the mag2torrent module to convert
                # magnet to torrent and then move it to the
                # proper watch folder
                print("Processing a magnet...")
                m2t.magnet2torrent(t_file, motogp_watch + motogp_title[0].replace(" ","") + ".torrent")

            update_json.updateJsonFile("motogp_update","No")
            update_json.updateJsonFile("motogp_rtorrent_email","No")
            send_email.send_email("TESTING AGAIN!!!",motogp[0])

    except:
        update_json.updateJsonFile("motogp_update","No")


    # Formula 1
    try:
        if(read_json.output_config()["formula1_title"] != str(formula1[0])):
            update_json.updateJsonFile("formula1_title",formula1[0])
            update_json.updateJsonFile("formula1_update","Yes")
            formula1_output = read_json.output_config()["formula1_title"]
            formula1_partition = (formula1_output.partition(":"))

            t = scrape(formula1_partition[2])
            t_title = t.torrent_title
            t_file = t.torrent_file


            # check if there is a file or just a magnet
            if(t_title[1] == "file"):
                # here we can proceed with the wget method since we have
                # an actual torrent file
                print("Processing a torrent file...")
                subprocess.call(["wget",t_file,"-P",formula1_watch])

            else:
                # here we need to run a different process
                # we can use the mag2torrent module to convert
                # magnet to torrent and then move it to the
                # proper watch folder
                print("Processing a magnet...")
                m2t.magnet2torrent(t_file, formula1_watch + formula1_title[0].replace(" ","") + ".torrent")

            update_json.updateJsonFile("formula1_update","No")
            update_json.updateJsonFile("formula1_rtorrent_email","No")
            send_email.send_email("New Formula 1 Race", formula1[0])

    except:
        update_json.updateJsonFile("formula1_update","No")

if __name__ == "__main__":
    main()
