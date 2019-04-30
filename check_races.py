#!/usr/bin/python3

import ettv_scrape
import scrape_torrent
import settings
import time

'''
First we need to run the ettv_scrape script
    this will update the json file with the newest info

Next we run the read_json script
    this will determine if the last entry of the list
    is the same as the current title for that race
If so, change the status to No and that's it.
If they are different, then update the title
    and change the status to Yes

Lastly, run the scrape_torrent script
    this script will look at the status
If the status of either or both are set to Yes,
    then download the torrent
'''

if __name__ == "__main__":

    ettv_scrape.main()

    if(settings.moto_partition[0] != settings.json_object.output_config()["motogp_title"]):
        settings.json_object.update_json("motogp_title", settings.moto_partition[0])
        settings.json_object.update_json("motogp_link", settings.moto_partition[2])
        settings.json_object.update_json("motogp_update","Yes")
        print("Updating MotoGP info...")
    else:
        settings.json_object.update_json("motogp_update","No")
        print("MotoGP imformation the same")

    if(settings.f1_partition[0] != settings.json_object.output_config()["formula1_title"]):
        settings.json_object.update_json("formula1_title",settings.f1_partition[0])
        settings.json_object.update_json("formula1_link",settings.f1_partition[2])
        settings.json_object.update_json("formula1_update","Yes")
        print("Updating F1 info...")
    else:
        settings.json_object.update_json("formula1_update","No")
        print("F1 information the same")

    scrape_torrent.grab_torrent()

