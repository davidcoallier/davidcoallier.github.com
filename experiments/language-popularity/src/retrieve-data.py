from __future__ import with_statement
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import json

# This is only to analyse the trend in popular language 
# in 2013. This can be easily adapted to work over the last
# 2 years.

base_archive_url = 'http://web.archive.org'

# 1. Retrieve the "list" of urls from archive.org. At the
#    moment, their JSON api is dead, so we parse the html.
search_url  = 'http://web.archive.org/web/20130101000000*/http://stackoverflow.com/tags'
search      = requests.get(search_url)
soup_search = BeautifulSoup(search.content)

days    = soup_search.findAll('a', {'title': '1 snapshots'})
history = defaultdict(dict)

for day in days:
    # We simply collect the href for future
    # use, and we also find the "date"
    href         = day['href']
    nominal_date = day['class'][0]

    # Now let's make the request with the retrieved url.
    url     = base_archive_url + href
    so_day  = requests.get(url)

    so_soup   = BeautifulSoup(so_day.content)
    cells     = so_soup.findAll('td', {'class': 'tag-cell'})
    langCount = []

    # Iterate over each tag-cell, and find the languages and their
    # counte per 24 hour slice.
    for cell in cells:
        hrefs = cell.findAll('a', {"class": "post-tag"})
        spans = cell.findAll('span', {"class": "item-multiplier-count"})
        ls = [href.contents[-1] for href in hrefs]
        cs = [int(count.string) for count in spans]
        langCount.append(dict(zip(ls, cs)))
    history[nominal_date] = langCount

# We just overwrite the output into history.json
with open('../web/data/history.json', 'w+') as f:
    f.write(json.dumps(history))
