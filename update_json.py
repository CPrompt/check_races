#!/usr/bin/python3

'''
    function to update the json file with
    either what we scrape from the site
    or setting the update to no
'''
import os
import json

feedData = os.path.dirname(os.path.realpath(__file__)) + "/static/config.json"

def updateJsonFile(json_key,json_value):
    jsonFile = open(feedData,"r")
    data = json.load(jsonFile)
    jsonFile.close()

    data[json_key] = json_value

    jsonFile = open(feedData, "w+")
    jsonFile.write(json.dumps(data,indent=4,sort_keys=True))
    jsonFile.close


