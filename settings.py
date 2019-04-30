#!/usr/bin/python3

'''
    Settings file to keeps all variables that are needed
    across each module
'''
import os
import Seymore
import settings
import requests
from urllib.request import Request, urlopen, urlretrieve

feedData = os.path.dirname(os.path.realpath(__file__)) + "/static/config.json"


page = Request("https://www.ettv.tv/user/smcgill1969/index.html", headers={'User-Agent': 'Mozilla5/0'})


json_object = Seymore.Audrey(feedData)


f1torrent_page = json_object.output_config()["formula1_link"]
motogp_page = json_object.output_config()["motogp_link"]

f1torrent_status = json_object.output_config()["formula1_update"]
motogp_status = json_object.output_config()["motogp_update"]

formula1_title = json_object.output_config()["formula1_title"]
motogp_title = json_object.output_config()["motogp_title"]

formula1_watch = json_object.output_config()["formula1_watch_directory_base"]
motogp_watch = json_object.output_config()["motogp_watch_directory_base"]

moto_output = json_object.output_config()["motogp_list"][0]
moto_partition = (moto_output.partition(":"))
f1_output = json_object.output_config()["f1_list"][0]
f1_partition = (f1_output.partition(":"))
