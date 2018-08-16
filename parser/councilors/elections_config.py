#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import json
import psycopg2
import ast
from sys import argv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import db_settings


conn = db_settings.con()
c = conn.cursor()
election_year = ast.literal_eval(argv[1])['election_year']

def parse_districts(county, districts):
    districts = re.sub(u'^(居住|【)', '', districts)
    category = re.search(u'(平地原住民|山地原住民)$', districts)
    districts = re.sub(u'(平地原住民|山地原住民)$', '', districts)
    if category:
        category = category.group()
    districts = re.sub(u'(】|之)', '', districts)
    l = []
    if districts:
        for district in districts.split(u'、'):
            if len(district) == 2:
                l = districts.split(u'、')
                break
            if not re.search(re.sub(u'[縣市]$', '', county), district):
                district = re.sub(u'[鄉鎮市區]$', '', district)
            l.append(district)
    return l, category
# update constituencies
constituencies = json.load(open('../../voter_guide/static/json/dest/constituencies_%s.json' % election_year))
counties = {}
for region in constituencies:
    if region['county'] not in counties.keys():
        counties.update({
            region['county']: {
                'regions': [],
                'duplicated': []
            }
        })
    districts_list, category = parse_districts(region['county'], region['district'])
    if category:
        if districts_list:
            district = u'%s（%s）' % (category, u'、'.join(districts_list))
        else:
            district = u'%s（%s）' % (category, u'全%s' % region['county'])
    else:
        district = u'、'.join(districts_list)
    counties[region['county']]['regions'].append({
        'constituency': region['constituency'],
        'districts_list': districts_list,
        'district': district,
        'category': category
    })
    c.execute('''
        update candidates_terms
        set district = %s
        where election_year = %s and county = %s and constituency = %s
    ''', (district, election_year, region['county'], region['constituency']))

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credential.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_key('10zFDmMF9CJDXSIENXO8iJXKE5CLBY62i_mSeqe_qDug')
worksheets = sh.worksheets()
for wks in worksheets:
    rows = wks.get_all_records()
    if wks.title == u'議員':
        for row in rows:
            print row['county'], row['constituency']
            if row['count_this']:
                counties[row['county']]['regions'][int(row['constituency'])-1]['elected_count_pre'] = row['count_pre']
                counties[row['county']]['regions'][int(row['constituency'])-1]['elected_count'] = row['count_this']
                counties[row['county']]['regions'][int(row['constituency'])-1]['reserved_seats'] = row['reserved_seats']
    else:
        continue

config = json.dumps({'constituencies': counties})
c.execute('''
    INSERT INTO elections_elections(id, data)
    VALUES (%s, %s)
    ON CONFLICT (id)
    DO UPDATE
    SET data = (COALESCE(elections_elections.data, '{}'::jsonb) || %s::jsonb)
''', [election_year, config, config])
conn.commit()

# update constituency_change
district_versions = json.load(open('../district_versions.json'))
config = json.dumps({'constituency_change': district_versions.get(election_year, {})})
c.execute('''
    INSERT INTO elections_elections(id, data)
    VALUES (%s, %s)
    ON CONFLICT (id)
    DO UPDATE
    SET data = (COALESCE(elections_elections.data, '{}'::jsonb) || %s::jsonb)
''', [election_year, config, config])
conn.commit()
