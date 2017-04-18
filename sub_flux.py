import time
import requests

def unlimit_get(url):
    response = requests.get(url);
    while (response.status_code == 429):
        time.sleep(2)
        response = requests.get(url)
    return response

data = []
start = time.time()
for i in range(60):
    subscribers = unlimit_get('https://www.reddit.com/r/askreddit/about.json').json()['data']['subscribers']
    data.append([time.time() - start, subscribers])
    print i
    time.sleep(2)

# now you can import matplotlib and start graphing :-)