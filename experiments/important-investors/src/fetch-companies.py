from __future__ import with_statement
import requests
import json
import sys
from pymongo import Connection

conn = Connection()
db = conn['exp003']
col = db['crunchbase']

url = 'http://api.crunchbase.com/v/1/company/%s.js?api_key=45aeg2jdjthnbw9yqf8exvrk'

with open('companies.json', 'r') as f:
    content = json.loads(f.read())

i = 1
for company in content[128518:]:
    try:
        res = requests.get(url % company['permalink'])

        if res.status_code in [404, 400]:
            i+= 1
            continue

        comp = res.json()
        col.insert(comp)
        if i % 100 == 0:
            print "Reached %s" % i
        i += 1
    except Exception, e:
        print "Caught exception at %s" % e
        i += 1
        continue
