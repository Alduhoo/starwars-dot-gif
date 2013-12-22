import base64
import json
import requests
import ConfigParser
import random
import os
import time
import subprocess

from twython import Twython
from base64 import b64encode
from makeGifs import makeGif
from makeGifs import loadChoices

config = ConfigParser.ConfigParser()
config.read("config.cfg")
config.sections()
CLIENT_ID = config.get("imgur", "client_id")
API_KEY = config.get("imgur", "api_key")
APP_KEY = config.get("twitter", "app_key")
APP_SECRET = config.get("twitter", "app_secret")
OAUTH_TOKEN = config.get("twitter", "oauth_token")
OAUTH_TOKEN_SECRET = config.get("twitter", "oauth_token_secret")

headers = {"Authorization": "Client-ID " + CLIENT_ID}
url = "https://api.imgur.com/3/upload.json"

movies_path = config.get("general", "movies_path")
subs_path = config.get("general", "subs_path")

# get choices
choices = loadChoices(movies_path, subs_path)

def reduceGif(filename):
    # first pass reduce the amount of colors
    if(os.path.getsize(filename) > 2097152):
        subprocess.call(['convert',
                        filename,
                        '-layers',
                        'Optimize',
                        '-colors',
                        '64',
                        filename])

    # other passes reduce the size
    while(os.path.getsize(filename) > 2097152):
        subprocess.call(['convert',
                        filename,
                        '-resize',
                        '90%',
                        '-coalesce',
                        '-layers',
                        'optimize',
                        filename])

def tweetGif(filename, quote):
    reduceGif(filename)
    try:
        response = requests.post(
            url,
            headers = headers,
            data = {
                'key': API_KEY,
                'image': b64encode(open(filename, 'rb').read()),
                'type': 'base64',
                'name': filename,
                'title': 'Random Dot Gif'
            }
        )
    except requests.exceptions.ConnectionError:
        # try again.
        tweetGif(filename, quote)


    try:
        res_json = response.json()
        link = res_json['data']['link']
    except ValueError:
        # try again.
        tweetGif(filename, quote)

    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    status = '"' + quote + '" ' + link + ' #randomgif'

    twitter.update_status(status=status)

if __name__ == '__main__':
    while True:
    	try:
    		choice = random.choice(choices)
    		quote = makeGif(choice, 0, rand=True)
    	except KeyboardInterrupt:
    		print "Ouch!"
    		exit()
    	except:
    		print "Unexpected error... trying again..."
    		print "tried to make gif from: " + str(choice)
    		continue

    	quote = ' '.join(quote)

    	print "tweeting..."
    	tweetGif('random.gif', quote)

    	print "sleeping..."
    	# sleep 1 hour
    	time.sleep(3600)
