#!/usr/bin/python -u

import time
import sys
import r_tools

def track_link(fullname, wait=10, end=60):
    t = 0
    while t < end:
        r = unlimit_get("https://www.reddit.com/by_id/t3_" + fullname + ".json")
        score = r.json()['data']['children'][0]['data']['score']
        data = str(t) + " " + str(score)
        print data
        time.sleep(wait)
        t = t + wait

# usage:
track_link('5zr471', 60, 18000)