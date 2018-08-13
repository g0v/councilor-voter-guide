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
import common


def updateCandidates(candidate):
    c.execute('''
        UPDATE candidates_candidates
        SET birth = %(birth)s
        WHERE uid = %(candidate_uid)s
    ''', candidate)
    c.execute('''
        UPDATE candidates_terms
        SET number = %(number)s, gender = %(gender)s, votes = %(votes)s, votes_percentage = %(votes_percentage)s, elected = %(elected)s, occupy = %(occupy)s
        WHERE candidate_id = %(candidate_uid)s AND election_year = %(election_year)s
    ''', candidate)

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
    df['elected'] = map(lambda x: True if re.search(u'[*!]', x) else False, df['elected'])
    df['occupy'] = map(lambda x: True if re.search(u'是', x) else False, df['occupy'])
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
        candidate['name'] = common.normalize_person_name(candidate['name'])
        candidate['name'] = re.sub(u'周鍾.*', u'周鍾㴴', candidate['name'])
        candidate['election_year'] = election_year
        candidate['candidate_uid'], created = common.get_or_create_candidate_uid(c, candidate)
        if created:
            updateCandidates(candidate)
        else:
            print(u'not exist candidate: %s' % candidate['name'])
            raise
conn.commit()
