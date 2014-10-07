#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import json
import psycopg2
from psycopg2.extras import Json
import pandas as pd
import db_settings


def uid(candidate):
    c.execute('''
        SELECT councilor_id, election_year
        FROM councilors_councilorsdetail
        WHERE name = %(name)s and county = %(county)s
        ORDER BY election_year DESC
    ''', candidate)
    r = c.fetchone()
    if r:
        return r
    c.execute('''
        SELECT councilor_id, election_year
        FROM councilors_councilorsdetail
        WHERE name = %(name)s
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
        WHERE county = %(county)s AND constituency = %(constituency)s
        ORDER BY election_year DESC
    ''', candidate)
    r = c.fetchone()
    if r:
        candidate['district'] = r[0]
    for key in ['education', 'experience', 'platform', 'remark']:
        if candidate.get(key):
            candidate[key] = '\n'.join(candidate[key])
    complement = {"election_year": '2014', "councilor_id":None, "birth":None, "gender":'', "party":'', "contact_details":None, "title":'', "district":'', "elected":None, "votes":None, "education":None, "experience":None, "remark":None, "image":'', "links":None, "platform":''}
    complement.update(candidate)
    c.execute('''
        INSERT into candidates_candidates(councilor_id, last_election_year, election_year, name, birth, gender, party, title, constituency, county, district, elected, contact_details, votes, education, experience, remark, image, links, platform)
        VALUES (%(uid)s, %(last_election_year)s, %(election_year)s, %(name)s, %(birth)s, %(gender)s, %(party)s, %(title)s, %(constituency)s, %(county)s, %(district)s, %(elected)s, %(contact_details)s, %(votes)s, %(education)s, %(experience)s, %(remark)s, %(image)s, %(links)s, %(platform)s)
    ''', complement)


conn = db_settings.con()
c = conn.cursor()
df = pd.read_excel(u'../../data/candidates_2014.xlsx', sheetname=0)
df = df[df['name'] != u'姓名']
df['party'] = map(lambda x: u'無黨籍' if re.search(u'^無$', x) else x, df['party'])
df['party'] = map(lambda x: u'臺灣團結聯盟' if re.search(u'台灣團結聯盟', x) else x, df['party'])
candidates = json.loads(df.to_json(orient='records'))
for candidate in candidates:
    match = re.search(u'(?P<county>\W+)第(?P<num>\d+)選(?:舉)?區', candidate['constituency'])
    candidate['county'] = match.group('county') if match else None
    candidate['constituency'] = match.group('num') if match else None
    if not (candidate['name'] and (re.search(u'(臺北市|臺中市|高雄市|新北市)', candidate['county']))):
        continue
    candidate['name'] = re.sub('\s', '', candidate['name'])
    candidate['name'] = re.sub(u'[•．]', u'‧', candidate['name'])
    candidate['uid'], candidate['last_election_year'] = uid(candidate)
    insertCandidates(candidate)
conn.commit()
