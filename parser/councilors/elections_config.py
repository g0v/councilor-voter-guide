#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import json
import psycopg2

import db_settings


conn = db_settings.con()
c = conn.cursor()
election_year = '2018'

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
config = json.dumps({'constituency_change': district_versions[election_year]})
c.execute('''
    INSERT INTO elections_elections(id, data)
    VALUES (%s, %s)
    ON CONFLICT (id)
    DO UPDATE
    SET data = (COALESCE(elections_elections.data, '{}'::jsonb) || %s::jsonb)
''', [election_year, config, config])
conn.commit()
