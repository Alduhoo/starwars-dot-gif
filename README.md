Star Wars DOT Gif
-------------

### To Use With Any Movie
Copy the contents of ```config.cfg.example``` into ```config.cfg``` and make sure to change the paths for VLC, the movies, and the sub files. This will look for available srt files allowing you to choose which movie to extract the quotes from. The movie name should be the same as the srt except for the extension.

To Run with search UI:
```
$ python movies.py
```

Running the twitter bot:

- make sure you create API accounts for both twitter and imgur
- update **config.cfg*** to have the keys for both
- run ```$ python twitter_bot.py```

The bot will tweet once every 60 minutes (1 hour).

Running the tumblr bot:

- make sure you create an API account for tumblr
- update **config.cfg** to have the keys and the blog url
- run ```$ python tumblr_bot.py```

### To Use
Copy the contents of ```config.cfg.example``` into ```config.cfg``` and make sure to change the paths for VLC and the Star Wars episodes. Any format that can be read by VLC should be acceptable for the movies. Note, if you don't plan on running the twitter bot you only need to fill out the general section of the cfg file.

To Run with search UI [(sample run)](http://www.youtube.com/watch?v=n387eBqnw1o):

The gif is created as the movie name + .gif: **Star Wars.gif**

```
$ python star_wars_gif.py
```


To get a random gif:

```
$ python makeGifs.py
```

If you want to use ```makeGifs``` elsewhere use:

```python
from makeGifs import makeGif
# source should be 4, 5, or 6
# index is the index of the SRT
makeGif(source, index)
```


**Note:** If generating gifs is taking too long for you remove ```nq=10``` from the ```writeGif``` call at the sacrifice of quality.
