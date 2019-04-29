#!/usr/bin/python3

import ettv_scrape
import read_json
import scrape_torrent
import update_json

'''
First we need to run the ettv_scrape script
    this will update the json file with the newest info
    that is scrapped from the ettv site

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
    read_json.main()
    scrape_torrent.grab_torrent()

