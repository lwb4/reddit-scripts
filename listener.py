import praw

client_id="reddit-client-id"
client_secret="reddit-client-secret"
username="bot_account"
password="password"
user_agent="user_agent by /u/username"

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     username=username,
                     password=password,
                     user_agent=user_agent)

# the keyword must be lowercase!
keyword = "reddit api"

for comment in reddit.subreddit(subs).stream.comments():
    if keyword in comment.body.lower():
        msg = comment.body + '\n\n' + str(comment.permalink())
        reddit.redditor('real_account').message("NEW COMMENT!", msg)
        print(msg)
        print("-----------------")