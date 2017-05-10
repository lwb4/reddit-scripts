# this script cross-posts submissions in which the TOP LEVEL COMMENT references another sub
# NOTE: you WILL be rate limited to posting submissions only once every ten minutes

import praw
import re

r = praw.Reddit(client_id='client-id',
                client_secret='client-secret',
                username='username',
                password='password',
                user_agent='your.user.agent.here (by /u/username)')

# regular expression for determining if a comment contains only a reference to another subreddit
regex = r"^\/r\/([a-zA-Z_0-9]+)$"

# look at every comment
# it'd be nice to only look at comments in sfw subs but idk how to do that
for comment in r.subreddit('all').stream.comments():
            
        # find the subreddit reference
        match = re.search(regex, comment.body)
        if match:
            
            sub = r.subreddit(match.group(1))
            
            # just catch all exceptions, print them to the screen, and keep going
            # the show must go on, as they say
            try:
                
                # check if it's a top level comment
                # and make sure it's not a NSFW post (Not Safe For Work)
                # not a strict requirement but I ain't about that life
                parent = comment.parent()
                if isinstance(parent, praw.models.Submission) \
                   and not(comment.subreddit.over18) \
                   and not(sub.over18):
                
                    # all conditions met
                    # formulate post, giving credit where it's due
                    print comment.permalink()
                    print "Attempting to cross-post..."
                    
                    title = "/u/" + str(parent.author) + " -- " + parent.title
                    submission = sub.submit(title, url=parent.url)
                    reply = "X-posted to /r/" + str(sub) + "\n\n" + "https://reddit.com" + submission.permalink
                    comment.reply(reply)
                    print "Success!"
                    print "--------"

            # I know this is a crappy exception handler but I don't care
            except Exception as e:
                print e
                print "--------"
                continue