import time
import random
import r_tools

laughs = ["ha", "he", "HA", "hee", "haw"]

while True:
    post = r_tools.unlimit_get('https://www.reddit.com/r/funny/new.json')
    fullname = 't3_' + post.json()['data']['children'][0]['data']['id']
    laugh = laughs[random.randint(0,len(laughs)-1)]
    comment_body = laugh*random.randint(1,15)
    data = {'parent': fullname, 'text': comment_body}
    headers = r_tools.get_access_headers(my_account)
    response = r_tools.unlimit_post('https://oauth.reddit.com/api/comment', data, headers)
    print response
    time.sleep(600)