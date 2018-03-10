#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import json
import codecs


# get_or_create village code maps
file_path = '../../data/candidates/village_code_2018.json'
if os.path.isfile(file_path):
    maps = json.load(open(file_path))
else:
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credential.json', scope)
    gc = gspread.authorize(credentials)
    sh = gc.open_by_key('1X0iuWD4Jrh1M-79X6FhtWOK1Tc4wY06N53E2wszWNBE')
    worksheets = sh.worksheets()
    for wks in worksheets:
        maps = {}
        rows = wks.get_all_values()[4:]
        for row in rows:
            row = rename_dict_key(row)
            if not row['new_village']:
                maps['%s_%s_%s' % (re.sub(u'台', u'臺', row['county_name']), row['town_name'], row['village_name'], )] = {
                    'county_code': row['county_code'],
                    'town_code': row['town_code'],
                    'village_code': row['village_code']
                }
            else:
                maps['_'.join(re.search(u'(.+?[縣市])(.+?[鄉鎮市區])(.+)', row['new_village']).groups())] = {
                    'town_code': row['village_code'][:7],
                    'village_code': row['village_code']
                }
    with codecs.open(file_path, 'w', encoding='utf-8') as outfile:
        outfile.write(json.dumps(maps, indent=2, ensure_ascii=False))

targets = json.load(open('../../data/cec/legislators_constituencies_2016.json'))
o = {x['constituency_label_wiki']: {
        'constituency_type_title': x['constituency_type_title'],
        'constituency_type': x['constituency_type'],
        'constituency_label_wiki': x['constituency_label_wiki'],
        'constituency_label': x['constituency_label'],
        'county': x['county'],
        'constituency_number': x['constituency_number'],
        'districts': {},
    }
    for x in targets
}
for target in targets:
    o[] = {
        'constituency_type_title': response.meta['meta']['constituency_type_title'],
        'constituency_type': response.meta['meta']['constituency_type'],
        'constituency_label_wiki': u'%s第%s選舉區' % (county, self.num_ref[constituency_number-1]),
        'constituency_label': u'%s第%02d選區' % (county, constituency_number),
        'county': county,
        'constituency_number': constituency_number,
        'district': m.group('district'),
        'villages': [],
    }
with codecs.open('../../data/cec/legislators_constituencies_2016_with_wikidata_id.json', 'w', encoding='utf-8') as outfile:
    outfile.write(json.dumps(targets, indent=2, ensure_ascii=False))
