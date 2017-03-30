# Join the community! https://www.reddit.com/r/redditscripting/
# (A community of one is still a community, right?)

# This script connects to a streaming endpoint using the Tweepy library
# Streaming APIs: https://dev.twitter.com/streaming/overview
# I used that instead of constantly polling the REST API.

import tweepy
import time

# A very short module with some basic functions, see:
# https://github.com/lincoln-b/reddit-scripts/blob/master/r_tools.py
import r_tools

# We need a LOT of authentication information for this to work

reddit_account = {
    "client_id": "reddit_app_client_id",
    "client_secret": "reddit_app_client_secret",
    "username": "reddit_username",
    "password": "reddit_password"
}

app_key = 'twitter_app_client_key'
app_secret = 'twitter_app__client_secret'
access_token = 'twitter_app_access_token'
access_secret = 'twitter_app_access_token_secret'

# use http://gettwitterid.com/ to get user ids from screen names
# Donald Trump          donaldtrump         736267842681602048
# Patton Oswalt         pattonoswalt        139162440
# Brendan Eich          brendaneich         9533042
# Rainn Wilson          rainnwilson         19637934
# Ken Jennings          kenjennings         234270825   

user_ids = ['736267842681602048', '139162440', '9533042', '19637934', '234270825']

# I made a few subreddits dedicated to tweet reposting
# When one of the users listed in user_ids makes a tweet

subreddits = {
    'donaldtrump': 'donald_trump_tweets',
    'brendaneich': 'brendaneich_tweets',
    'rainnwilson': 'rainnwilson_tweets',
    'kenjennings': 'kenjennings_tweets'
}

# This is the class that actually handles tweets that come in from the streaming endpoint.

class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        try:
            data = {
                'title': status.text,
                'kind': 'link',
                'sr': subreddits[status.user.screen_name.lower()],
                'url': 'https://twitter.com/' + status.user.screen_name + '/status/' + status.id_str
            }

            # Get a new access token each time, because it might expire
            headers = r_tools.get_access_headers(reddit_account)
            response = r_tools.unlimit_post('https://oauth.reddit.com/api/submit', data, headers)
            
            print data['title']
            print data['sr']
            print response
            print '---------'
        
        except KeyError:
            # For some reason, a bunch of other random tweets show up
            # that aren't by ANY of the users specified in user_ids.
            # Not sure why. But this at least keeps track of them.
            print 'Received screen_name: ' + status.user.screen_name
            print '---------'

    def on_error(self, status_code):
        print(str(status_code))
        print '---------'

        # When we get a 420, wait a minute and reconnect
        # https://dev.twitter.com/streaming/overview/connecting
        if status_code == 420:
            return False

# Now, actually start the thing:
# It's bad practice to try-catch all errors, but this code produces some weird exceptions that I don't know about.
# Needs to be looked into by more experienced eyes.

# Followed the guide at https://www.dataquest.io/blog/streaming-data-python/ to set this up

while True:
    try:
        auth = tweepy.OAuthHandler(app_key, app_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)

        stream_listener = StreamListener()
        stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
        stream.filter(follow=user_ids)

        # The only way this code gets reached is if StreamListener returns false.
        # And the only way StreamListener returns false is if it gets rate limited.
        print "Rate limited by Twitter, waiting one minute to reconnect..."
        time.sleep(60)
    except:
        print "Error, waiting thirty seconds to restart."
        time.sleep(30)

