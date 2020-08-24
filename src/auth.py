# Tokens
CONSUMER_KEY        = 'NULL'
CONSUMER_SECRET     = 'NULL'
ACCESS_TOKEN        = 'NULL'
ACCESS_TOKEN_SECRET = 'NULL'

# Setup
TWITTER_ACCOUNT = "NULL"       # Name of the account you're tweeting to.
DEBUG = False	# Setting this to False will start tweeting live.
ODDS = 6	# How often should the bot run? (8 = 1/8 times)
ORDER = 2	# How sensical should the bot be? (2 = low and 4 = high)

# Sources
SOURCE_TWITTER = [""]		# List of Twitter accounts from which to generate tweets.
SOURCE_URL = ['']	        # List of websites from which to generate tweets.
SOURCE_TEXT = "sample_text.txt"			# Name of a text file from which to generate tweets.

# Settings
SOURCE_EXCLUDE = r'^$'          # Text that matches this regexp will not be processed.
USE_WEB = True			        # Setting this to True will have the bot listed websites for content.
USE_TEXT = False             	# Setting this to True will test tweet generation from a static file.
WEB_CONTEXT = ['span', 'h2']	# List of the tags or objects to search for in the list of websites.
WEB_ATTRIBUTES = [{'class': 'example-text'}, {}] # List of dictionaries containing the attributes for each page.
ENABLE_STATUS_SOURCES = True	# Fetch twitter statuses as source
ENABLE_STATUS_POSTING = True	# Tweet resulting status
