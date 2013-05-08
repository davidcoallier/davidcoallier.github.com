from __future__ import with_statement, division
from collections import defaultdict
from operator import itemgetter
from dateutil import parser
from datetime import datetime
import numpy as np
import time
import json
import sys

def changePercent(llist):
    new = []
    for a, b in zip(llist[::1], llist[1::1]):
        new.append(100 * (int(b) - int(a)) / int(a))
    return new 

csv = {"header": None, "content": []}
with open('../data/history.json', 'r') as f:
    history = json.loads(f.read())

# We'll just parse all the keys and their dates.
keys = []
for entry in history:
    keys.append(parser.parse(entry))

ordered = []
keys = sorted(keys) # Now we sort by date.

# Here we basically retrieve the sorted keys
# transform the values back into the format
# the history's keys are formatted in, and recreate
# the ordered keys.
for key in keys:
    tmp_time = datetime.strftime(key, '%b-%-d-%Y')
    ordered.append({tmp_time:history[tmp_time]})


headKeys = [datetime.strftime(key, '%b-%-d-%Y') for key in keys]
csv['header'] = 'lang,%s' % ','.join(headKeys)

langs = defaultdict(list)
for key in headKeys:
    # Find each lang value for timestamp
    for line in ordered:
        if key in line:
            for lang in line[key]: 
                for lang, count in lang.items():
                    langs[lang].append(str(count))

ratio = defaultdict(list)
for lang in langs:
    ratio[lang] = changePercent(langs[lang])

for lang, countlist in ratio.items():
    csv['content'].append(str(lang) + ',' + ','.join((str(x) for x in countlist)))

csv = csv['header'] + '\n' + '\n'.join(csv['content'])

with open('../data/so_history.csv', 'w+') as f:
    f.write(csv)

# Let's try using nvd3...
json_payload = []

for lang, countlist in ratio.items():
    tmp = {}
    tmp['key'] = lang
    tmp['values'] = []
    countlist = countlist[1:]
    for pos, key in enumerate(keys):
        if pos > len(countlist)-1:
            continue
        val = countlist[pos]
        tmp_time = datetime.strftime(key, '%s')
        tmptmp = [tmp_time, val]
        tmp['values'].append(tmptmp)
        tmp['disabled'] = True

    json_payload.append(tmp)

json_payload = sorted(json_payload, key=itemgetter('key')) 
with open('../data/so_history.json', 'w+') as f:
    f.write(json.dumps(json_payload))

# I have no idea how to do this with d3... I've tried and I dont' have
# enough time to keep dicking around like an eejit so I'm doing it in python.
new_payload = []
for key, js in enumerate(json_payload):
    vals = js['values']
    sumVal = np.cumsum([v[1] for k, v in enumerate(vals)]) 
    new_vals = map(list, zip([v[0] for k, v in enumerate(vals)], sumVal))

    new_payload.append({
        'key': js['key'],
        'disabled': js['disabled'],
        'values': new_vals
    })


new_payload = sorted(new_payload, key=itemgetter('key')) 
with open('../data/so_cumsum.json', 'w+') as f:
    f.write(json.dumps(new_payload))

