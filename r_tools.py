import requests
import re
import random
import time

user_agent = "chrome:com.whatever.script:v1 (by /u/reddituser)"

# make a get request
# loop until the request goes through
# useful if you're being rate-limited!
def unlimit_get(url):
    response = requests.get(clean_url(url));
    i = 0
    while (response.status_code == 429 and i < 10):
        print "Rate limited on " + url
        print "Waiting one second..."
        time.sleep(1)
        response = requests.get(url)
        i = i + 1
    return response

# same as unlimit_get but for POST requests
def unlimit_post(url, data, headers):
    response = requests.post(clean_url(url), data=data, headers=headers)
    i = 0
    while (response.status_code == 429 and i < 10):
        print "Rate limited on " + url
        print "Waiting one second..."
        time.sleep(1)
        response = requests.post(url, data=data, headers=headers)
        i = i + 1
    return response

# these next two functions expect sample data like the following:
user = {
    "client_id": "thisismyclientid",
    "client_secret": "thisismyclientsecret",
    "username": "reddituser",
    "password": "redditpassword"
}

def get_access_token(user):
    client_auth = requests.auth.HTTPBasicAuth(user["client_id"], user["client_secret"])
    post_data = {"grant_type": "password", "username": user["username"], "password": user["password"]}
    headers = {"User-Agent": user_agent}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    return response.json()
# usage: 
# data = {'fullname': 't3_whatever', 'text': 'I am a comment!'}
# headers = get_access_headers(user)
# response = r_tools.unlimit_post('https://oauth.reddit.com/api/comment', data, headers)
def get_access_headers(user):
    response_json = get_access_token(user)
    return {"Authorization": response_json['token_type'] + " " + response_json['access_token'],
            "User-Agent": user_agent}
