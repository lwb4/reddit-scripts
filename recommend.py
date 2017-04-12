import praw
import spotipy
import spotipy.util as util
import re
import time

# Useful links:
# Spotify API Endpoint Reference: https://developer.spotify.com/web-api/endpoint-reference/
# Spotify Authorization Guide: https://developer.spotify.com/web-api/authorization-guide/
# spotipy docs: http://spotipy.readthedocs.io/en/latest/

client_id="reddit-client-id"
client_secret="reddit-client-secret"
username="username"
password="password"
user_agent="user_agent by /u/username"

r = praw.Reddit(client_id=client_id,
                client_secret=client_secret,
                username=username,
                password=password,
                user_agent=user_agent)

# NOTE: you may have to export these first to get util.prompt_for_user_token to work:
# export SPOTIPY_CLIENT_ID='spotify-client-id'
# export SPOTIPY_CLIENT_SECRET='spotify-client-secret'
# export SPOTIPY_REDIRECT_URI='http://localhost/'
# (these values found at: https://developer.spotify.com/my-applications/)

# This is how you obtain an access token for the Spotify API:
token = util.prompt_for_user_token('Firstname Lastname', 'user-library-read')
sp = spotipy.Spotify(auth=token)

# Regular expression to match music submission titles on /r/Music
# regexes are never pretty :(
regex = r"^([\w\s\/\.,&\+']+ - [\w\s\/\.,&\+\"]+).*\[[\w\s\/\.,&\+'-]+\]$"

for submission in r.subreddit("music").stream.submissions():
    # 1. Form a search query from the submission
    # 2. Search for that track in Spotify
    # 3. Look for recommendations based on that track's ID
    # 4. Formulate a comment with the recommended tracks
    match = re.search(regex, submission.title)
    if match:
        results = sp.search(q=match.group(1))
        if results['tracks']['items']:
            comment = "Based on this track, Spotify recommends the following tracks:\n\n"
            id = results['tracks']['items'][0]['id']
            recommendations = sp.recommendations(seed_tracks=[id],limit=8)
            for track in recommendations['tracks']:
                song = track['name']
                artist = track['artists'][0]['name']
                link = track['external_urls']['spotify']
                comment = comment + "* [" + song + " - " + artist + "](" + link + ")\n"
            try:
                submission.reply(comment)
                print "--------------"
                print comment
            except:
                print "Rate limited, waiting ten minutes..."
                time.sleep(600)
