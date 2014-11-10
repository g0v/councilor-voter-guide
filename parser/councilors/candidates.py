#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import json
import glob
import psycopg2
from psycopg2.extras import Json
import pandas as pd
import db_settings


def latest_term(candidate):
    c.execute('''
        SELECT councilor_id, election_year
        FROM councilors_councilorsdetail
        WHERE name = %(name)s and county = %(previous_county)s and election_year < %(election_year)s
        ORDER BY election_year DESC
    ''', candidate)
    r = c.fetchone()
    if r:
        return r
    c.execute('''
        SELECT councilor_id, election_year
        FROM councilors_councilorsdetail
        WHERE name = %(name)s and election_year < %(election_year)s
        ORDER BY election_year DESC
    ''', candidate)
    r = c.fetchone()
    if r:
        return r
    # non-cht in name
    m = re.match(u'(?P<cht>.+?)[a-zA-Z]', candidate['name'])
    candidate['name_like'] = m.group('cht') if m else candidate['name']
    c.execute('''
        SELECT councilor_id, election_year
        FROM councilors_councilorsdetail
        WHERE name like %(name_like)s and county = %(previous_county)s and election_year < %(election_year)s
        ORDER BY election_year DESC
    ''', candidate)
    r = c.fetchone()
    if r:
        return r
    c.execute('''
        SELECT councilor_id, election_year
        FROM councilors_councilorsdetail
        WHERE name like %(name_like)s and election_year < %(election_year)s
        ORDER BY election_year DESC
    ''', candidate)
    r = c.fetchone()
    if r:
        return r
    return None, None

def insertCandidates(candidate):
    c.execute('''
        SELECT district
        FROM councilors_councilorsdetail
        WHERE county = %(previous_county)s AND constituency = %(constituency)s
        ORDER BY election_year DESC
    ''', candidate)
    r = c.fetchone()
    if r:
        candidate['district'] = r[0]
    for key in ['education', 'experience', 'platform', 'remark']:
        if candidate.get(key):
            candidate[key] = '\n'.join(candidate[key])
    complement = {"councilor_id":None, "birth":None, "gender":'', "party":'', "contact_details":None, "title":'', "district":'', "elected":None, "votes":None, "education":None, "experience":None, "remark":None, "image":'', "links":None, "platform":''}
    complement.update(candidate)
    c.execute('''
        INSERT into candidates_candidates(councilor_id, last_election_year, election_year, name, birth, gender, party, title, constituency, county, district, elected, contact_details, votes, education, experience, remark, image, links, platform)
        VALUES (%(uid)s, %(last_election_year)s, %(election_year)s, %(name)s, %(birth)s, %(gender)s, %(party)s, %(title)s, %(constituency)s, %(county)s, %(district)s, %(elected)s, %(contact_details)s, %(votes)s, %(education)s, %(experience)s, %(remark)s, %(image)s, %(links)s, %(platform)s)
    ''', complement)


conn = db_settings.con()
c = conn.cursor()
election_year = '2014'
county_versions = json.load(open('../county_versions.json'))
files = [f for f in glob.glob('../../data/candidates/%s/*.xlsx' % election_year)]
for f in files:
    df = pd.read_excel(f, sheetname=0, names=['date', 'constituency', 'name', 'party'], usecols=[0, 1, 2, 3])
    df = df[df['name'] != u'姓名']
    df['party'] = map(lambda x: u'無黨籍' if re.search(u'^無$', x) else x, df['party'])
    df['party'] = map(lambda x: u'臺灣團結聯盟' if re.search(u'台灣團結聯盟', x) else x, df['party'])
    candidates = json.loads(df.to_json(orient='records'))
    for candidate in candidates:
        match = re.search(u'(?P<county>\W+)第(?P<num>\d+)選(?:舉)?區', candidate['constituency'])
        candidate['county'] = match.group('county') if match else None
        candidate['constituency'] = match.group('num') if match else None
        if not (candidate['name'] and (re.search(u'(臺北市|臺中市|高雄市|新北市|臺南市|新竹市|彰化縣|宜蘭縣|桃園市)', candidate['county']))):
            continue
        for county_change in county_versions[election_year]:
            candidate['previous_county'] = county_change['from'] if candidate['county'] == county_change['to'] else candidate['county']
        candidate['name'] = re.sub('\s', '', candidate['name'])
        candidate['name'] = re.sub(u'[・•．]', u'‧', candidate['name'])
        candidate['election_year'] = election_year
        candidate['uid'], candidate['last_election_year'] = latest_term(candidate)
        insertCandidates(candidate)
conn.commit()
