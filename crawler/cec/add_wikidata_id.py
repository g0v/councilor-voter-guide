#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import json
import codecs


maps = json.load(open('query.json'))
targets = json.load(open('councilors_constituencies_2014.json'))
for target in targets:
    for r in maps:
        if r['itemLabel'] == target['constituency_label_wiki']:
            target['wikidata_item'] = r['item']
            break
with codecs.open('councilors_constituencies_2014_with_wikidata_id.json', 'w', encoding='utf-8') as outfile:
    outfile.write(json.dumps(targets, indent=2, ensure_ascii=False))
