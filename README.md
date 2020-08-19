## FlawBOT.Twitter

A Twitter bot written in Python, originally made by [Tom Meagher](https://github.com/tommeagher) for [heroku_ebooks](https://github.com/tommeagher/heroku_ebooks). This bot currently runs on a RaspberryPi and posts tweets to [@mannco_ebooks](https://twitter.com/mannco_ebooks) at pseudorandom intervals. This project requires [Python 3](https://www.python.org/downloads/), [python-twitter](https://github.com/bear/python-twitter) and [BeautifulSoup4](https://github.com/wention/BeautifulSoup4).

## Setup
[Clone this repo](https://github.com/CriticalFlaw/FlawBOT.Twitter/archive/master.zip) and modify the included **auth.py** file, adding your Twitter tokens which you can get [here](https://developer.twitter.com/en). After you've set everything up, start the bot with `sudo python3 ebooks.py`. For more information, check out [heroku_ebooks](https://github.com/tommeagher/heroku_ebooks#heroku_ebooks).

To have the bot script run on a schedule, enter `sudo crontab -e` into the Terminal and add the following line at the bottom of the file:

`*/30 * * * * sudo python3 /home/pi/flawbot.twitter/ebooks.py >> /home/pi/flawbot.twitter/logs.txt 2>&1`

This line will make the bot run every half an hour and log its output. For more crontab examples, go [here](https://crontab.guru/examples.html).
