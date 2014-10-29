#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import glob
import json
import codecs
from scrapy.selector import Selector
from numpy import nan
import db_settings


def write_file(data, file_name):
    file = codecs.open(file_name, 'w', encoding='utf-8')
    file.write(data)

def is_number(text):
    try:
        float(text)
        return True
    except:
        return False

def getIdList(name_list, election_year, county):
    c.execute('''
        SELECT id
        FROM councilors_councilorsdetail
        WHERE name IN %s and election_year = %s and county = %s
    ''', (tuple(name_list), election_year, county))
    r = c.fetchall()
    if r:
        return r[0]
    for name in name_list:
        print '"%s"' % name

def select_all_councilors(election_year, county):
    c.execute('''
        SELECT id
        FROM councilors_councilorsdetail
        WHERE election_year = %s and county = %s
    ''', (election_year, county))
    return [x[0] for x in c.fetchall()]

def get_election_year(suggestion):
    c.execute('''
        SELECT election_year
        FROM councilors_councilorsdetail
        WHERE county = %(county)s
        GROUP BY election_year
        ORDER BY election_year desc
    ''', suggestion)
    r = c.fetchall()
    for election_year in r:
        if int(suggestion['suggest_year']) >= int(election_year[0]):
            return election_year[0]

conn = db_settings.con()
c = conn.cursor()
files = [f for f in glob.glob('../../data/*/suggestions/*.xml')]
for f in files:
    f = open(f, 'r')
    print f.name
    sel = Selector(text=f.read())
    county = sel.xpath('//table/tr[1]/td[1]/p/text()').re(u'\S*?[縣市]')[0]
    year, month = re.sub('\D', ' ', sel.xpath('//table/tr[2]/td[1]/p/text()').extract()[0]).split()
    suggestions, rownum = [], 1
    for tr in sel.xpath('//table/tr[count(td)>6 and count(td)<10]'):
        row = dict(zip(['councilor', 'suggestion', 'position', 'suggest_expense', 'approved_expense', 'expend_on', 'brought_by', 'bid_type', 'bid_by'], tr.xpath('td/p/text()').extract()))
        row['county'] = county
        row['suggest_year'] = str(int(year) + 1911)
        row['suggest_month'] = month
        row['election_year'] = get_election_year(row)
        if re.search(u'等.*議員', row['councilor']):
            row['councilor_ids'] = select_all_councilors(row['election_year'], row['county'])
        else:
            row['councilor'] = re.sub(u'(副?議長|議員|)', '', row['councilor'])
            row['councilor'] = re.sub(u'[・•．]', u'‧', row['councilor'])
            row['councilor'] = re.sub(u'、', ' ', row['councilor'])
            row['councilor_ids'] = getIdList(common.getNameList(row['councilor']), '2010', county) if row['councilor'] else nan
        row['suggest_expense'] = float(re.sub(u'[^\d.]', '', row['suggest_expense']))
        row['approved_expense'] = float(re.sub(u'[^\d.]', '', row['approved_expense']))
        row['suggest_expense'] = row['suggest_expense']*1000 if is_number(row['suggest_expense']) else nan
        row['approved_expense'] = row['approved_expense']*1000 if is_number(row['approved_expense']) else nan
        row['uid'] = '%s-%d-%d' % (county, int(year)+1911, rownum)
        suggestions.append(row)
        rownum += 1
    dump_data = json.dumps(suggestions, sort_keys=True, indent=4, ensure_ascii=False)
    write_file(dump_data, re.sub('xml$', 'json', f.name))
