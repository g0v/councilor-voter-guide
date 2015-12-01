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

import db_settings


def updateCandidates(candidate):
    c.execute('''
        SELECT *
        FROM candidates_candidates
        WHERE name = %(name)s and election_year = %(election_year)s and county = %(county)s
    ''', candidate)
    key = [desc[0] for desc in c.description]
    r = c.fetchone()
    if r:
        complement = dict(zip(key, r))
    else:
        # non-cht in name
        m = re.match(u'(?P<cht>.+?)[a-zA-Z]', candidate['name'])
        print m
        candidate['name_like'] = '%s%%' % m.group('cht') if m else '%s%%' % candidate['name']
        c.execute('''
            SELECT *
            FROM candidates_candidates
            WHERE name like %(name_like)s and election_year = %(election_year)s and county = %(county)s
        ''', candidate)
        key = [desc[0] for desc in c.description]
        r = c.fetchone()
        if r:
            complement = dict(zip(key, r))
        else:
            for k, v in candidate.items():
                print '"%s" "%s"' % (k, v)
            raw_input()
    for key in ['education', 'experience', 'platform', 'remark']:
        if candidate.has_key(key):
            candidate[key] = '\n'.join(candidate[key])
    complement.update(candidate)
    c.execute('''
        UPDATE candidates_candidates
        SET birth = %(birth)s, number = %(number)s, gender = %(gender)s, votes = %(votes)s, votes_percentage = %(votes_percentage)s, elected = %(elected)s
        WHERE id = %(id)s
    ''', complement)

conn = db_settings.con()
c = conn.cursor()
election_year = '2014'
# After election, update info that didn't exist before election
files = [f for f in glob.glob('../../data/candidates/%s/after_election/*/*.xls' % election_year)]
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
        print candidate['area']
        candidate['area'] = re.sub(u'選舉?區', u'', candidate['area'])
        match = re.search(u'第(?P<constituency>\d+)', candidate['area'])
        if match:
            candidate['constituency'] = int(match.group('constituency'))
            candidate['county'] = re.sub(u'第\d+', '', candidate['area'])
        else:
            candidate['constituency'] = 1
            candidate['county'] = candidate['area']
        if candidate['county'] == u'澎湖縣':
            continue
        # normalize_person
        candidate['name'] = re.sub('\s', '', candidate['name'])
        candidate['name'] = re.sub(u'[。˙・･•．.]', u'‧', candidate['name'])
        if candidate['name'] == u'笛布斯顗賚':
            candidate['name'] = u'笛布斯‧顗賚'
        candidate['name'] = re.sub(u'黄', u'黃', candidate['name'])
        candidate['name'] = re.sub(u'眞', u'真', candidate['name'])
        candidate['name'] = re.sub(u'周鍾.*', u'周鍾㴴', candidate['name'])
        for case in [(u'臺中市', 15, u'温建華', u'溫建華'), (u'新竹市', 4, u'李姸慧', u'李妍慧'), (u'嘉義縣', 1, u'王啓澧', u'王啟澧'), (u'彰化縣', 1, u'黄育寬', u'黃育寬'), (u'彰化縣', 2, u'陳秀寳', u'陳秀寶'), (u'苗栗縣', 5, u'鍾福貴', u'鍾褔貴'), (u'臺南市', 9, u'林慶鎭', u'林慶鎮'), ]:
            if (candidate['county'], candidate['constituency'], candidate['name']) == case[:3]:
                candidate['name'] = case[3]
        #
        updateCandidates(candidate)
conn.commit()
