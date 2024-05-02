#! /usr/bin/env python3

import requests
import sys


data = requests.get('https://climatereanalyzer.org/clim/sst_daily/json/oisst2.1_world2_sst_day.json')

result = {}
for d in data.json():
    if len(d['name']) != 4:
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

for key, value in sorted(result.items()):
    print ("{}\t{:.2f}\t{:.2f}".format(key,value['highest'], value['lowest']))
