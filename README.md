# check_races

This script monitors the page on ettv for the MotoGP and F1 races uploaded by a single user SMcGill1969.

### Process:
What I entended the use for this, was to have a more automated way to see if there was a new race
without having to continually refresh the page.  So in this case, I wanted the script to monitor
the page for me, and if there is a new race, send a text message.  Then, once the race was downloaded
and ready to watch, send a message for notification.

### More in depth:

We are monitoring a specific page that is specified in the initial file (check\_races.py)
The script uses BeautifulSoup to scrape the page and look for the section where the torrents are listed.
(table table-hover table-bordered).

All of that information is added to a list that we then loop over to find which ones contain the words in the "key\_word" list.
From there, we scrape out the "title" and the "href"

Once that informatin is scraped, we determine if the title contains "MotoGP" or "Formula.1" and add each to their appropriate lists.

At this point, we can use the information grabbed and see if it matches what is in the "static/config.json" file.
If they are the same, do nothing.  It they are different add the title and the href information to the json file.
The result will be something like :

```
"Formula.1.2019x04.Azerbaijan.Race.SkyF1HD.SD : https://ettv.tv/torrent/388430/formula-1-2019x04-azerbaijan-race-skyf1hd-sd"
```

The href portion contains the page where the torrent link is.  Since this is a new torrent, we scrape that page using the function "scrape\_page"

The last step is to simply use wget to download the torrent file that is linked.  We specify the directory in the "static/config.json" file for each differnt race.
From there, rtorrent is used to download the file.

Rtorrent can also send notification when a download is complete.  To do this we can simply use a bash file to call the "send\_email.py" script.  That is the reason the call to main
reads the json file so that the name of the race comes through in the text message.

### A bit of manual configs:
First you will need to create a python file called simply "creds.py" and place in the "loginfo" directory.
This is a simple python dictionary in this format, and a sample is in the repo:

```python
login = {
	"fromEmail": "<YOUR EMAIL>",
	"toEmail": "<THE PHONE NUMBER TO SEND THE TEXT>",
	"emailLogin": "<SMTP LOGIN USER>",
	"emailPass": "<SMTP LOGIN PASSWORD>",
	"emailServer": "<SMTP SERVER>",
	"emailPort": "<SMTP SERVER PORT>"												}
```

In the file "static/config.json", you will need to specify the directories you would like the downloads to end up.

```python
"formula1_watch_directory_base": "/path/to/f1/watch/folder"
```

Then I have a cron set to run every 1/2 hour only on Sundays because...that's Race Day!
(i.e. ``*/30 * * * 0 python3 /path/to/scrtip/raceUpdate.py``)

