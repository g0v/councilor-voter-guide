#!/usr/bin/python
# -*- coding: utf-8 -*
import re
import json
import codecs
from datetime import datetime


def write_file(data, file_name):
    file = codecs.open(file_name, 'w', encoding='utf-8')
    file.write(data)
    file.close()

objs = json.load(open('tncc/tnccp/tnccp.json'))
l = []
for obj in objs:
    d = obj['each_terms'][0]
    d['name'] = obj['name']
    d['birth'] = datetime(*map(int, obj['birth'].split('/'))).strftime('%Y-%m-%d')
    d['district'] = re.sub(u'\.', u'、', d['district'])
    m = re.search(u'(副?議長)。?$', d['experience'][0])
    d['title'] = m.group(1) if m else u'議員'
    d['county'] = u'臺南市'
    l.append(d)
dump_data = json.dumps(l, sort_keys=True, indent=4, ensure_ascii=False)
write_file(dump_data, 'tncc/councilors.json')
dump_data = json.dumps(l, sort_keys=True, indent=4, ensure_ascii=False)
write_file(dump_data, 'pretty_format/tncc/councilors.json')
