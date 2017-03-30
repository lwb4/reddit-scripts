import sys

# You MUST create an empty comment.log in the same directory where you run this script
# There's probably an easy way to do that in python but I don't know it

print "Welcome to Quote_Bot v0.0.1!"
print "----------------------------"

print "Importing PRAW modules..."

import praw
from praw.models import Comment

print "Authenticating with Reddit..."

reddit = praw.Reddit(client_id='your client id here',
                     client_secret='your client secret here',
                     username='your username here',
                     password='your password here',
                     user_agent='your user agent here')

print "Ready to start!"
print "Processing submissions, please stand by."

already_commented = []

# read in the already-commented-on fullnames

log = open("comment.log", "r")
already_commented = log.readlines()
already_commented = [x.strip() for x in already_commented]
log.close()

# close and re-open the file for writing

log = open("comment.log", "a+")

quote_key = "don't quote me on this, but "
quote_key_length = len(quote_key)

while True:
    num = 0
    for submission in reddit.subreddit('all').hot(limit=200):
        for comment in submission.comments.list():
            if isinstance(comment, Comment):
                if quote_key in comment.body.lower():
                    if comment.fullname not in already_commented:
                        quote = comment.body[comment.body.find(quote_key)+quote_key_length:]
                        body = "\"" + quote + "\"\n\n -" + str(comment.author)
                        comment.reply(body)
                        print body
                        num = num + 1
                        already_commented.append(comment.fullname)
                        log.write(comment.fullname + "\n")

log.close()