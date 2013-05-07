from __future__ import with_statement
from collections import defaultdict
from dateutil import parser
from datetime import datetime
import json

csv = {"header": None, "content": []}
with open('../web/data/history.json', 'r') as f:
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


keys = [datetime.strftime(key, '%b-%-d-%Y') for key in keys]
csv['header'] = 'lang,%s' % ','.join(keys)

langs = defaultdict(list)
for key in keys:
    # Find each lang value for timestamp
    for line in ordered:
        if key in line:
            for lang in line[key]: 
                for lang, count in lang.items():
                    langs[lang].append(str(count))

for lang, countlist in langs.items():
    csv['content'].append('%s,%s' % (lang, ','.join(countlist)))

csv = csv['header'] + '\n' + '\n'.join(csv['content'])

with open('../web/data/so_history.csv', 'w+') as f:
    f.write(csv)
