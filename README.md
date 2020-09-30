![img](https://i.imgur.com/YlbST5I.jpg)

A Twitter bot written in Python, originally made by [Tom Meagher](https://github.com/tommeagher) for [heroku_ebooks](https://github.com/tommeagher/heroku_ebooks). This bot currently runs on a RaspberryPi and posts tweets to [@tf2_ebooks](https://twitter.com/tf2_ebook) at pseudorandom intervals. This project requires [Python 3](https://www.python.org/downloads/), [python-twitter](https://github.com/bear/python-twitter) and [BeautifulSoup4](https://github.com/wention/BeautifulSoup4).

## Setup
[Clone this repo](https://github.com/CriticalFlaw/FlawBOT.Twitter/archive/master.zip) and modify the included **auth.py** file, adding your Twitter tokens which you can get [here](https://developer.twitter.com/en). After you've set everything up, start the bot with `sudo python3 ebooks.py`. For more information, check out [heroku_ebooks](https://github.com/tommeagher/heroku_ebooks#heroku_ebooks).

To have the bot script run on a schedule, enter `sudo crontab -e` into the Terminal and add the below line at the bottom of the file. This will execute the script every 30 minutes and log its output to a separate file. For more crontab examples, go [here](https://crontab.guru/examples.html).

`*/60 * * * * sudo python3 /home/pi/FlawBOT.Twitter/ebooks.py >> /home/pi/FlawBOT.Twitter/logs.txt 2>&1`
