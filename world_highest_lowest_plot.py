#! /usr/bin/env python3

import requests
import sys
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


data = requests.get('https://climatereanalyzer.org/clim/sst_daily/json/oisst2.1_world2_sst_day.json')

result = {}
for d in data.json():
    if len(d['name']) != 4 or d['name'] == '1981':
        # 1981 wasn't complete
        continue

    if d['name'] not in result:
        result[d['name']] = {}
        result[d['name']]['highest'] = None
        result[d['name']]['lowest'] = None

    for e in d['data']:
        if e is not None:
            if result[d['name']]['highest'] == None or result[d['name']]['highest'] < e:
                result[d['name']]['highest'] = e

            if result[d['name']]['lowest'] == None or result[d['name']]['lowest'] > e:
                result[d['name']]['lowest'] = e


plotdata = []
thisyear = datetime.now().strftime('%Y')
for r in result:
    highest = result[r]['highest']
    lowest = result[r]['lowest']

    # Lowest temperature is usually reached at the end of the year.
    special1 = None
    special2 = None
    if r == thisyear:
        special1 = lowest
        special2 = highest
        highest = None
        lowest = None

    plotdata.append({'year': r, 'highest': highest, 'lowest': lowest, 'special1': special1, 'special2': special2})


df = pd.DataFrame(plotdata)
ax = df.plot(x='year', y=['highest', 'special2', 'lowest', 'special1'], xlabel='Year', ylabel='Temperature in °C', style=['.','.','.','.'], title="SST per Year", color=["#c44141", "#fc7e7e", "#326fa8", "#49e0e3"])
plt.legend(['Highest', 'Highest {} (preliminiary)'.format(thisyear), 'Lowest', 'Lowest {} (preliminary)'.format(thisyear)])

ax.figure.savefig('output/world_highest_lowest.png')
