import sys
from sys import argv
import requests
import json
import os
import datetime

def download(url):
    filename = url.split('/')[-1]
    if (os.path.isfile(filename) && os.stat(filename).st_size > 0):
        print ("File {} already downloaded".format(filename))
        return False
    else:
        print ("Download from {}".format(url))
        with open(filename, "wb") as file:
            file.write(requests.get(url).content)

        if os.stat(filename).st_size == 0:
            print ("Empty file, remove")
            os.remove(filename)
            return False
        else:
            print ("File {} downloaded correctly".format(filename))
            return True

def toShortDate(iso8601datetime):
    parsed = datetime.datetime.strptime(iso8601datetime[:19], '%Y-%m-%dT%H:%M:%S')
    return str(parsed.year)[2:] + '{:0>2}'.format(str(parsed.month)) + '{:0>2}'.format(str(parsed.day))

if len(argv) != 3:
    print ("Wrong parameters, expected start and end index")
else:
    start = int(argv[1])
    end = int(argv[2])
    for number in range (start, end):
        link = "https://www.kcrw.com/music/shows/henry-rollins/kcrw-broadcast-{}/player.json".format(number)
        raw = requests.get(link).text
        if raw.startswith('{'):
            parsed = json.loads(raw)
            media = parsed['media']
            if (len(media) == 0):
                print ("Media not available for show #{} trying to download in other way...".format(number))
                shortdate = toShortDate(parsed['airdate'])
                download("https://podcast-download.kcrw.com/kcrw/audio/podcast/music/hr/hr{}KCRW_Broadcast_{}.mp3".format(shortdate, number))
                download("https://kcrw-od.streamguys1.com/kcrw/audio/website/music/hr/hr{}kcrw_broadcast_{}.mp3".format(shortdate, number))
                download("https://kcrw-od.streamguys1.com/kcrw/audio/website/music/hr/KCRW-henry_rollins-kcrw_broadcast_{}.mp3".format(number))
            else:
                print ("Media available for show #{}".format(number))
                download(media[0]['url'])
        else:
            print ("Not a json")
            download("https://kcrw-od.streamguys1.com/kcrw/audio/website/music/hr/KCRW-henry_rollins-kcrw_broadcast_{}.mp3".format(number))
