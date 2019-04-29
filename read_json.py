#!/usr/bin/python3
import os
import json
from update_json import *
import settings

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
    returned_list = read_json(settings.feedData)
    config_dict = use_list(returned_list)
    return config_dict

def main():

    moto_output = output_config()["motogp_list"][0]
    moto_partition = (moto_output.partition(":"))
    f1_output = output_config()["f1_list"][0]
    f1_partition = (f1_output.partition(":"))

    if(moto_partition[0] != output_config()["motogp_title"]):
        updateJsonFile("motogp_title", moto_partition[0])
        updateJsonFile("motogp_link", moto_partition[2])
        print("Updating MotoGP info...")
        updateJsonFile("motogp_update","Yes")
    else:
        print("MotoGP imformation the same")
        updateJsonFile("motogp_update","No")

    if(f1_partition[0] != output_config()["formula1_title"]):
        updateJsonFile("formula1_title",f1_partition[0])
        updateJsonFile("formula1_link",f1_partition[2])
        print("Updating F1 info...")
        updateJsonFile("formula1_update","Yes")
    else:
        print("F1 information the same")
        updateJsonFile("formula1_update","No")



if __name__ == "__main__":
    main()



