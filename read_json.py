#!/usr/bin/python3

'''
    functions to read the json config file
    this is where we store all the info about the race
    and if it's new or not
'''

import json
import os

feedData = os.path.dirname(os.path.realpath(__file__)) + "/static/config.json"

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

if __name__ == "__main__":
    motogp_title = output_config()["motogp_title"]
    print(type(motogp_title))
