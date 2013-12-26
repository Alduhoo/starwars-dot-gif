import random
import os
import ConfigParser
import time
import subprocess
import re

from tumblpy import Tumblpy
from makeGifs import makeGif
from makeGifs import loadChoices

config = ConfigParser.ConfigParser()
config.read("config.cfg")
config.sections()

CONSUMER_KEY = config.get("tumblr", "consumer_key")
CONSUMER_SECRET = config.get("tumblr", "consumer_secret")
OAUTH_TOKEN = config.get("tumblr", "oauth_token")
OAUTH_TOKEN_SECRET = config.get("tumblr", "oauth_token_secret")
BLOG_URL = config.get("tumblr", "blog_url")

movies_path = config.get("general", "movies_path")
subs_path = config.get("general", "subs_path")

# get choices
choices = loadChoices(movies_path, subs_path)

t = Tumblpy(
	CONSUMER_KEY,
	CONSUMER_SECRET,
	OAUTH_TOKEN,
	OAUTH_TOKEN_SECRET,
)

def reduceGif(filename):
	# reduce amount of colors, because tumblr sucks
	subprocess.call(['convert',
					filename,
					'-layers',
					'Optimize',
					'-colors',
					'64',
					filename])
	while(os.path.getsize(filename) > 1048576):
		subprocess.call(['convert',
						filename,
						'-resize',
						'90%',
						'-coalesce',
						'-layers',
						'Optimize',
						filename])

def postGif(filename, quote, tags):
	reduceGif(filename)

	photo = open(filename, 'rb')

	post = t.post('post', blog_url=BLOG_URL, params={'type':'photo', 'caption': quote, 'data': photo, 'tags': ', '.join(tags)})

if __name__ == '__main__':
	while True:
		choice = random.choice(choices)
		tags = []
		try:
			quote = makeGif(choice, 0, rand=True, frames=20)
		except KeyboardInterrupt:
			print "Ouch..."
			exit()
		except:
			print "Unexpected error..."
			print "was trying to make gif from: " + str(choice)
			continue
		quote = ' '.join(quote)
		m = re.search('\s\(\d\d\d\d\)', choice['name'])
		if m != None:
			title = choice['name'][:m.start()]
		else:
			m = re.search('\sS\d\dE\d\d', choice['name'])
			if m != None:
				title = choice['name'][:m.start()]
				tags = tags + [choice['name'][m.start():m.end()]]
			else:
				title = choice['name'][:choice['name'].find('.')]

		print "posting to tumblr -> " + title + "..."
		tags = ['randomDOTgif', 'gif', title] + tags
		postGif('random.gif', quote, tags)

		print "sleeping..."
		# sleep
		time.sleep(900)
