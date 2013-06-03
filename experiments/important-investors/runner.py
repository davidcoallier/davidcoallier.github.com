from pymongo import Connection

con = Connection()
db = con['exp003']
col = db['crunchbase']

cats = col.distinct("category_code")
print ';'.join(['python graph-investors.py %s' % cat for cat in cats])
