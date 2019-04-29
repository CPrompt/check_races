#!/usr/bin/python3
import os
import json
import settings

# function used to update the json file with the info we get from the scrape
def updateJsonFile(json_key,json_value):
    jsonFile = open(settings.feedData,"r")
    data = json.load(jsonFile)
    jsonFile.close()

    data[json_key] = json_value

    jsonFile = open(settings.feedData, "w+")
    jsonFile.write(json.dumps(data,indent=4,sort_keys=True))
    jsonFile.close
