from pymongo import Connection

con = Connection()
db = con['exp003']
col = db['crunchbase']

cats = col.distinct("category_code")
print ';'.join(['python graph-investors.py %s' % cat for cat in cats])
print
for cat in cats:
    if cat is None:
        continue
    print '<div class="group" id="%s">' % cat
    print '  <h2>%s Investors</h2>' % cat.title()
    print '  <div class="chart"></div>'
    print '  <div class="table"></div>'
    print '</div>'

print
print
for cat in cats:
    print '    drawGraph("%s")' % cat
    print '    drawTable("%s")' % cat

