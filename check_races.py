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
    functions to read the json config file
    this is where we store all the info about the race
    and if it's new or not
'''
def read_json(myFeed):
    try:
        json_data = open(myFeed)
        data = json.load(json_data)
    except:
        print("Can't open")
    return data

def use_list(passed_list):
    return passed_list

def output_config():
    returned_list = read_json(feedData)
    config_dict = use_list(returned_list)
    return config_dict


'''
    function to update the json file with
    either what we scrape from the site
    or setting the update to no
'''
def updateJsonFile(json_key,json_value):
    jsonFile = open(feedData,"r")
    data = json.load(jsonFile)
    jsonFile.close()

    data[json_key] = json_value

    jsonFile = open(feedData, "w+")
    jsonFile.write(json.dumps(data,indent=4,sort_keys=True))
    jsonFile.close


'''
    function to actually scrape where the torrent is from
    the link that we read from the json file
'''

def scrape_page(page):
    global torrent_file

    page = Request(page,headers={'User-Agent': 'Mozilla5/0'})
    webpage = urlopen(page).read()
    soup = BeautifulSoup(webpage,'html.parser')
    for a in soup.find_all("a", {"class":"download_link file"}):
        torrent_file = a['href']
        return(torrent_file)


'''
    Main function will simply scrape the page finding where the MotoGP and F1 info is for Races, 2019 and in SD
    Then we are going to grab that info and update the list in the JSON file /static/config.json
    The config.json file is used to determine if the latest race is new or not
'''
def main():

    formula1_watch = output_config()["formula1_watch_directory_base"]
    motogp_watch = output_config()["motogp_watch_directory_base"]

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
                    else:
                            formula1.append(torrent_title + " : " + "https://ettv.tv" + torrent_link)


    if(output_config()["motogp_title"] != str(motogp[0])):
        updateJsonFile("motogp_title",motogp[0])
        updateJsonFile("motogp_update","Yes")
        motogp_output = output_config()["motogp_title"]
        motogp_partition = (motogp_output.partition(":"))

        scrape_page(motogp_partition[2])
        subprocess.call(["wget",torrent_file,"-P",motogp_watch])
        updateJsonFile("motogp_update","No")

    else:
        return

    if(output_config()["formula1_title"] != str(formula1[0])):
        updateJsonFile("formula1_title",formula1[0])
        updateJsonFile("formula1_update","Yes")
        formula1_output = output_config()["formula1_title"]
        formula1_partition = (formula1_output.partition(":"))

        scrape_page(formula1_partition[2])
        subprocess.call(["wget",torrent_file,"-P",formula1_watch])
        updateJsonFile("formula1_update","No")

    else:
        return


if __name__ == "__main__":
    main()
