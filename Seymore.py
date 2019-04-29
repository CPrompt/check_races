#!/usr/bin/python3

import json


'''
USAGE:


   - myfile.json:
        {
            "title":"HotDog"
        }


    - Calling Module:

import json_read_write

myobject = Seymore.Audrey('myfile.json')


myobject.update_json("title","HotDog")
print(myobject.output_config()["title"])

myobject.update_json("title","Not HotDog")
print(myobject.output_config()["title"])
'''

class Audrey(object):


    def __init__(self,feedData):
        self.feedData = feedData



    # Reading and outputting info from JSON file
    def read_json(self,myFeed):
        try:
            json_data = open(myFeed)
            data = json.load(json_data)
        except:
            print("Can't open")
            exit(0)
        else:
            return data


    def use_list(self,passed_list):
        return passed_list


    def output_config(self):
        try:
            returned_list = self.read_json(self.feedData)
            config_dict = self.use_list(returned_list)
        except:
            print("Error returning dictionary")
            exit(0)
        else:
            return config_dict



    # Writing data to JSON file
    def update_json(self,json_key,json_value):
        try:
            jsonFile = open(self.feedData,"r+")
        except:
            print("Can't open feed for writing")
            exit(0)
        else:
            data = json.load(jsonFile)
            data[json_key] = json_value
        finally:
            jsonFile.close()


        try:
            jsonFile = open(self.feedData, "w+")
        except:
            print("Could not open file for writing")
        else:
            jsonFile.write(json.dumps(data,indent=4,sort_keys=True))
        finally:
            jsonFile.close
