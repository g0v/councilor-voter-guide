#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
import uuid
import json
import glob
from datetime import datetime

import pandas as pd

import common
import db_settings


def get_or_create_uid(councilor):
    '''
        return councilor_uid, created
    '''
    councilor['councilor_ids'] = tuple(common.GetCouncilorId(c, councilor['name']))
    if not councilor['councilor_ids']:
        return (uuid.uuid4().hex, False)
    c.execute('''
        SELECT councilor_id
        FROM councilors_councilorsdetail
        WHERE councilor_id in %(councilor_ids)s AND county = %(county)s
        ORDER BY
            CASE
                WHEN election_year = %(election_year)s AND constituency = %(constituency)s AND name = %(name)s THEN 1
                WHEN election_year = %(election_year)s AND constituency = %(constituency)s THEN 2
                WHEN constituency = %(constituency)s AND name = %(name)s THEN 3
                WHEN constituency = %(constituency)s THEN 4
                WHEN name = %(name)s THEN 5
            END,
            election_year DESC
        LIMIT 1
    ''', councilor)
    r = c.fetchone()
    return (r[0], True) if r else (uuid.uuid4().hex, False)

def Councilors(councilor):
    councilor['former_names'] = councilor.get('former_names', [])
    variants = set()
    for variant in [(u'勳', u'勲'), (u'溫', u'温'), (u'黃', u'黄'), (u'寶', u'寳'), (u'真', u'眞'), (u'福', u'褔'), (u'鎮', u'鎭'), (u'妍', u'姸'), (u'市', u'巿'), (u'衛', u'衞'), (u'館', u'舘'), (u'峰', u'峯'), (u'群', u'羣'), (u'啟', u'啓'), (u'鳳', u'鳯'), (u'冗', u'宂'), (u'穀', u'榖'), (u'曾', u'曽'), (u'賴', u'頼'), (u'蒓', u'莼'), ]:
        variants.add(re.sub(variant[0], variant[1], councilor['name']))
        variants.add(re.sub(variant[1], variant[0], councilor['name']))
    councilor['identifiers'] = list((variants | set(councilor['former_names']) | {councilor['name'], re.sub(u'[\w‧]', '', councilor['name']), re.sub(u'\W', '', councilor['name']).lower(), }) - {''})
    councilor['former_names'] = '\n'.join(councilor['former_names'])
    complement = {"birth": None}
    complement.update(councilor)
    c.execute('''
        INSERT INTO councilors_councilors(uid, name, birth, former_names, identifiers)
        VALUES (%(uid)s, %(name)s, %(birth)s, %(former_names)s, %(identifiers)s)
        ON CONFLICT (uid)
        DO UPDATE
        SET name = %(name)s, birth = %(birth)s, former_names = %(former_names)s, identifiers = %(identifiers)s
    ''', complement)

def insertCouncilorsDetail(councilor):
    for key in ['education', 'experience', 'platform', 'remark']:
        if councilor.has_key(key) and type(councilor[key]) is list:
            councilor[key] = '\n'.join(councilor[key])
    complement = {"gender": '', "party": '', "contact_details": None, "title": u'議員', "constituency": None, "county": '', "district": '', "in_office": True, "term_start": None, "term_end": {}, "education": None, "experience": None, "remark": None, "image": '', "links": None, "platform": ''}
    complement.update(councilor)
    c.execute('''
        INSERT INTO councilors_councilorsdetail(councilor_id, election_year, name, gender, party, title, constituency, county, district, in_office, contact_details, term_start, term_end, education, experience, remark, image, links, platform)
        VALUES (%(uid)s, %(election_year)s, %(name)s, %(gender)s, %(party)s, %(title)s, %(constituency)s, %(county)s, %(district)s, %(in_office)s, %(contact_details)s, %(term_start)s, %(term_end)s, %(education)s, %(experience)s, %(remark)s, %(image)s, %(links)s, %(platform)s)
        ON CONFLICT (councilor_id, election_year)
        DO UPDATE
        SET name = %(name)s, gender = %(gender)s, party = %(party)s, title = %(title)s, constituency = %(constituency)s, in_office = %(in_office)s, contact_details = %(contact_details)s, county = %(county)s, district = %(district)s, term_start = %(term_start)s, term_end = %(term_end)s, education = %(education)s, experience = %(experience)s, remark = %(remark)s, image = %(image)s, links = %(links)s, platform = %(platform)s
    ''', complement)

conn = db_settings.con()
c = conn.cursor()
election_year = '2009'
# After election, update info that didn't exist before election
files = [f for f in glob.glob('../../data/candidates/%s/after_election/*/*.xls' % '2014')]
for f in files:
    print f
    col_indexs = ['area', 'name', 'number', 'gender', 'birth', 'party', 'votes', 'votes_percentage', 'elected', 'occupy']
    df = pd.read_excel(f, sheetname=0, names=col_indexs, usecols=range(0, len(col_indexs)))
    df = df[df['name'].notnull()]
    df['area'] = df['area'].fillna(method='ffill') # deal with merged cell
    df['elected'] = map(lambda x: True if re.search(u'[*]', x) else False, df['elected'])
    candidates = json.loads(df.to_json(orient='records'))
    for candidate in candidates:
        candidate['election_year'] = election_year
        candidate['birth'] = datetime.strptime(str(candidate['birth']), '%Y')
        candidate['area'] = re.sub(u'選舉?區', u'', candidate['area'])
        match = re.search(u'第(?P<constituency>\d+)', candidate['area'])
        if match:
            candidate['constituency'] = int(match.group('constituency'))
            candidate['county'] = re.sub(u'第\d+', '', candidate['area'])
        else:
            candidate['constituency'] = 1
            candidate['county'] = candidate['area']
        if candidate['county'] != u'澎湖縣':
            continue
        if candidate['occupy'] == u'是':
            if re.search(u'無黨籍', candidate['party']):
                candidate['party'] = u'無黨籍'
            candidate['name'] = common.normalize_person_name(candidate['name'])
            candidate['uid'], created = get_or_create_uid(candidate)
            print candidate['uid'], created
            Councilors(candidate)
            insertCouncilorsDetail(candidate)
conn.commit()
