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
from scrapy.selector import Selector

import common


county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
county = common.county_abbr2string(county_abbr)
election_year = common.election_year(county)
county_abbr3 = common.county2abbr3(county)
for file in glob.glob(u'../../../data/%s/meeting_minutes/%s/xml/*.xml' % (county_abbr, election_year)):
    with codecs.open(file, 'r', encoding='utf-8') as f:
        print f.name
        fileName, fileExt = os.path.splitext(os.path.basename(f.name))
        xml_text = unicodedata.normalize('NFC', f.read())
        x = Selector(text=xml_text, type='xml')
        x.remove_namespaces()
        print x.xpath(u'//Row/Cell/Data//text()').re(u"一覽表\((\d+)/")
        for node in x.xpath(u'//Row/Cell[Data[re:test(., "^日期$")]]'):
            for date in node.xpath('following-sibling::Cell//text()').extract():
                print date
