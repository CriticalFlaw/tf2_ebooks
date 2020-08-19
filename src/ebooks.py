import random
import re
import sys
import twitter
import markov
from bs4 import BeautifulSoup
from html.entities import name2codepoint as n2c
from urllib.request import urlopen
from auth import *
#from twython import Twython

# Simple Version
#message = "Hello world!"
#twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
#twitter.update_status(status=message)
#print("Tweeted: {}".format(message)


def connect():
    # Use Twitter
    return twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET, tweet_mode='extended')
    # Use Twython
    #twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SEC$
    #return None


def entity(text):
    if text[:2] == "&#":
        try:
            if text[:3] == "&#x":
                return chr(int(text[3:-1], 16))
            else:
                return chr(int(text[2:-1]))
        except ValueError:
            pass
    else:
        guess = text[1:-1]
        if guess == "apos":
            guess = "lsquo"
        numero = n2c[guess]
        try:
            text = chr(numero)
        except KeyError:
            pass
    return text


def filter_status(text):
    text = re.sub(r'\b(RT|MT) .+', '', text)		# Remove anything after RT or MT.
    text = re.sub(r'(\#|@|(h\/t)|(http))\S+', '', text)	# Remove URLs, hashtags, HTS, etc.
    text = re.sub('\s+', ' ', text)			# Consolidate whitespaces into single space.
    text = re.sub(r'\"|\(|\)', '', text)		# Remove quotes and attributes.
    text = re.sub(r'\s+\(?(via|says)\s@\w+\)?', '', text)
    text = re.sub(r'<[^>]*>','', text)			# Remove HTML tags from mastodon posts. (TODO: Remove?)
    htmlsents = re.findall(r'&\w+;', text)
    for item in htmlsents:
        text = text.replace(item, entity(item))
    text = re.sub(r'\xe9', 'e', text)			# Remove accented letter e
    return text


def scrape_page(src_url, web_context, web_attributes):
    tweets = []
    last_url = ""
    for i in range(len(src_url)):
        if src_url[i] != last_url:
            last_url = src_url[i]
            print(">>> Scraping {0}".format(src_url[i]))
            try:
                page = urlopen(src_url[i])
            except Exception:
                last_url = "ERROR"
                import traceback
                print(">>> Error scraping {0}:".format(src_url[i]))
                print(traceback.format_exc())
                continue
            soup = BeautifulSoup(page, 'html.parser')
        hits = soup.find_all(web_context[i], attrs=web_attributes[i])
        if not hits:
            print(">>> No results found!")
            continue
        else:
            errors = 0
            for hit in hits:
                try:
                    tweet = str(hit.text).strip()
                except (UnicodeEncodeError, UnicodeDecodeError):
                    errors += 1
                    continue
                if tweet:
                    tweets.append(tweet)
            if errors > 0:
                print(">>> We had trouble reading {} result{}.".format(errors, "s" if errors > 1 else ""))
    return(tweets)


def grab_tweets(api, max_id=None):
    source_tweets = []
    user_tweets = api.GetUserTimeline(screen_name=user, count=200, max_id=max_id, include_rts=True, trim_user=True, exclude_replies=True)
    if user_tweets:
        max_id = user_tweets[-1].id - 1
        for tweet in user_tweets:
            if tweet.full_text:
                tweet.text = filter_status(tweet.full_text)
            else:
                tweet.text = filter_status(tweet.full_text)
            if re.search(SOURCE_EXCLUDE, tweet.text):
                continue
            if tweet.text:
                source_tweets.append(tweet.text)
    else:
        pass
    return source_tweets, max_id


if __name__ == "__main__":
    order = ORDER
    guess = 0
    if ODDS and not DEBUG:
        guess = random.randint(0, ODDS - 1)

    if guess:
        print("Sorry, not this time.")
        sys.exit()
    else:
        api = connect()
        source_statuses = []
        if USE_TEXT:
            file = SOURCE_TEXT
            print(">>> Generating from {0}".format(file))
            string_list = open(file).readlines()
            for item in string_list:
                source_statuses += item.split(",")
        if USE_WEB:
            source_statuses += scrape_page(SOURCE_URL, WEB_CONTEXT, WEB_ATTRIBUTES)
        if ENABLE_STATUS_SOURCES and SOURCE_TWITTER and len(SOURCE_TWITTER[0]) > 0:
            twitter_tweets = []
            for handle in SOURCE_TWITTER:
                user = handle
                handle_stats = api.GetUser(screen_name=user)
                status_count = handle_stats.statuses_count
                max_id = None
                my_range = min(17, int((status_count/200) + 1))
                for x in range(1, my_range):
                    twitter_tweets_iter, max_id = grab_tweets(api, max_id)
                    twitter_tweets += twitter_tweets_iter
                print("{0} tweets found in {1}".format(len(twitter_tweets), handle))
                if not twitter_tweets:
                    print("Error fetching tweets from Twitter. Aborting.")
                    sys.exit()
                else:
                    source_statuses += twitter_tweets
        if len(source_statuses) == 0:
            print("No statuses found!")
            sys.exit()
        mine = markov.MarkovChainer(order)
        for status in source_statuses:
            if not re.search('([\.\!\?\"\']$)', status):
                status += "."
            mine.add_text(status)
        for x in range(0, 10):
            ebook_status = mine.generate_sentence()

        # Randomly drop the last word, as horse_ebooks appears to do.
        if random.randint(0, 4) == 0 and re.search(r'(in|to|from|for|with|by|our|of|your|around|under|beyond)\s\w+$', ebook_status) is not None:
            print("Oops. Lost the last word.")
            ebook_status = re.sub(r'\s\w+.$', '', ebook_status)
            print(ebook_status)

        # Add an additional sentence if the initial tweet is too short.
        if ebook_status is not None and len(ebook_status) < 40: #TODO: Minimum length should be settable by user
            rando = random.randint(0, 10)
            if rando == 0 or rando == 7:
                print("Short tweet. Adding another random sentence.")
                newer_status = mine.generate_sentence()
                if newer_status is not None:
                    ebook_status += " " + mine.generate_sentence()
                else:
                    ebook_status = ebook_status
            elif rando == 1:
                print("or you can take it up with me!")
                ebook_status = ebook_status.upper()

        # Remove tweets that match their sources.
        if ebook_status is not None and len(ebook_status) < 210:
            for status in source_statuses:
                if ebook_status[:-1] not in status:
                    continue
                else:
                    print("TOO SIMILAR: " + ebook_status)
                    sys.exit()

            if not DEBUG:
                status = api.PostUpdate(ebook_status)
            print(ebook_status)

        elif not ebook_status:
            print("Status is empty, sorry.")
        else:
            print("TOO LONG: " + ebook_status)
