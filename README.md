An Ebooks Twitter bot written in Python, originally created by [Tom Meagher](https://github.com/tommeagher) for [heroku_ebooks](https://github.com/tommeagher/heroku_ebooks). This bot is running on a RaspberryPi, posting tweets to [@tf2_ebook](https://twitter.com/tf2_ebook) at pseudorandom intervals. This project requires [Python 3](https://www.python.org/downloads/), [python-twitter](https://github.com/bear/python-twitter) and [BeautifulSoup4](https://github.com/wention/BeautifulSoup4).

1. Clone the repository and update the included **auth.py** file with your Twitter [access tokens](https://developer.twitter.com/en).
```
git clone https://github.com/CriticalFlaw/tf2_ebooks.git
sudo nano tf2_ebooks/auth.py
```
2. Install project dependancies and run the bot.
```
sudo apt-get install python3-pip
sudo pip3 install python-twitter
sudo pip3 install beautifulsoup4
sudo python3 ebooks.py
```
3. Schedule the bot to run every hour using crontab.
```
sudo crontab -e
*/60 * * * * sudo python3 /home/pi/tf2_ebooks/ebooks.py >> /home/pi/tf2_ebooks/logs.txt 2>&1
```
