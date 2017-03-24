from HTMLParser import HTMLParser
from html2text import html2text
from collections import Counter, OrderedDict
import re
import sys
import operator
import r_tools

# usage:
# python get_all_comments.py redditusername
# this program scans all the comments they have ever made,
# scans through, and outputs a list of their top 50 most common used words

user = sys.argv[1]
after = ''
word_bank = []
h = HTMLParser()

while True:
    if after is None:
        break
    append = ''
    if after != '':
        append = '?after=' + after
    response = r_tools.unlimit_get('https://www.reddit.com/user/' + user + '/comments.json' + append)
    after = response.json()['data']['after']
    comments_page = response.json()['data']['children']
    for comment in comments_page:
        comment_html = h.unescape(comment['data']['body_html'])
        comment_text = re.sub('[^A-Za-z0-9\'\-]', ' ', html2text(comment_html)).split()
        for word in comment_text:
            word_bank.append(word.lower())

word_use = Counter(sorted(word_bank))
most_used = sorted(word_use.items(), key=operator.itemgetter(1), reverse=True)
for usage in most_used[:50]:
    print usage[0] + " " + str(usage[1])