#! /usr/bin/env python3

import requests
import sys


data = requests.get('https://climatereanalyzer.org/clim/sst_daily/json/oisst2.1_natlan1_sst_day.json')

for d in data.json():
    if d['name'] != '2024':
        continue

    result = None
    for e in d['data']:
        if e is None:
            print("Last SST value is: {}".format(result))
            sys.exit(0)
        else:
            result = e


