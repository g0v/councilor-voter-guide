#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import json
import codecs


query = '''
    SELECT ?item ?itemLabel ?city ?cityLabel WHERE {
        ?item wdt:P31 wd:Q49924492;
            wdt:P17 wd:Q865;
            wdt:P131 ?city .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "zh-tw". }
    }
    order by ?itemLabel
'''
generator = pg.WikidataSPARQLPageGenerator(query, site=wikidata_site)
position_maps = {page.get()['labels']['zh-tw']: page.id for page in generator}
json.dump(position_maps, open('taiwan/data/councilor_position_maps.json', 'w'), indent=2, ensure_ascii=False)

target = json.load(open('../../data/candidates/county_district_2018.json'))
for area in target:

with codecs.open('../../data/candidates/election_region_with_village_code_2018.json', 'w', encoding='utf-8') as outfile:
    outfile.write(json.dumps(target, indent=2, ensure_ascii=False))
