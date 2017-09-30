#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../../')
import os
import re
import json
import glob
import codecs
import unicodedata
from collections import defaultdict
from scrapy.selector import Selector

import db_settings
import common
import vote_common


def normalize_record(x):
    if x and re.search(u'[0oO○〇]', x):
        return True

Session_Token = re.compile(u'''
    (?P<name>
        第\s*(?P<ad>\d+)\s*屆
        第\s*(?P<session>\d+)\s*次(?P<type>(定期|臨時))大?會
    )
''', re.X)

conn = db_settings.con()
c = conn.cursor()
county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
county = common.county_abbr2string(county_abbr)
election_year = common.election_year(county)
county_abbr3 = common.county2abbr3(county)
for file in glob.glob(u'../../../data/%s/meeting_minutes/%s/html/*.html' % (county_abbr, election_year)):
    with codecs.open(file, 'r', encoding='utf-8') as f:
        print f.name
        fileName, fileExt = os.path.splitext(os.path.basename(f.name))
        xml_text = unicodedata.normalize('NFC', f.read())
        x = Selector(text=xml_text, type='html')
        x.remove_namespaces()
        year = int(x.xpath('//text()').re(u'表\s*[（(](\d+)/\d+/\d+')[0]) + 1911
        d = {}
        for table in x.xpath(u'//table'):
            days = table.xpath('descendant::tr[1]/td//text()').re('(\d+/\d+)')
            dates = ['%d-%02d-%02d' % (year, int(day.split('/')[0]), int(day.split('/')[1])) for day in days]
            for tr in table.xpath('descendant::tr[td[1][re:test(., "^\d+$")]]'):
                name = re.sub(u'[．﹒]', u'‧', tr.xpath('td[2]//text()').extract_first() or '')
                if not name:
                    continue
                records = [normalize_record(x.xpath('descendant-or-self::*/text()').extract_first()) for x in tr.xpath('td[position()>2]')]
                for date, showup in zip(dates, records):
                    if showup:
                        d.setdefault(date, {'present': [], 'absent': []})['present'].append(name)
                    else:
                        d.setdefault(date, {'present': [], 'absent': []})['absent'].append(name)
        # clean holiday records
        for date, v in d.items():
            if len(v['present']) == 0:
                d.pop(date)
        sorted(d, key=lambda x: x[0])
        match = Session_Token.search(re.sub(u'、', '', f.name))
        for i, (k, v) in enumerate(d.items(), 1):
            if match.group('type') == u'定期':
                uid = '%s-%s-%02d-CS-%02d' % (county_abbr3, election_year, int(match.group('session')), i)
            elif match.group('type') == u'臨時':
                uid = '%s-%s-T%02d-CS-%02d' % (county_abbr3, election_year, int(match.group('session')), i)
            sitting_dict = {
                'county': county,
                'election_year': election_year,
                'uid': uid,
                'name': u'%s第%d次會議' % (re.sub('\s', '', match.group('name')), i),
                'date': k
            }
            common.InsertSitting(c, sitting_dict)
            common.FileLog(c, sitting_dict['name'])
            common.Attendance(c, sitting_dict, ' '.join(v['present']), 'CS', 'present')
            common.Attendance(c, sitting_dict, ' '.join(v['absent']), 'CS', 'absent')
vote_common.person_attendance_param(c, county)
conn.commit()
