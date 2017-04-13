import praw

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

# iterate through most recent 100 comments
# delete any comments in which another thread also has a comment by the same author

for comment in r.redditor(username).comments.new(limit=100):
    for other_comment in comment.parent().comments:
        if (comment.author.name == other_comment.author.name) and (comment.fullname != other_comment.fullname):
            other_comment.delete()
            print "found one"