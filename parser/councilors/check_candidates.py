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


def in_office(candidate):
    candidate['name'] = re.sub('\s', '', candidate['name'])
    candidate['name'] = re.sub(u'[˙・•．]', u'‧', candidate['name'])
    for case in [(u'新竹市', '4', u'李姸慧', u'李妍慧'), (u'臺南市', '9', u'林慶鎭', u'林慶鎮'), ]:
        if (candidate['county'], candidate['constituency'], candidate['name']) == case[:3]:
            candidate['name'] = case[3]
    c.execute('''
        SELECT councilor_id
        FROM candidates_candidates
        WHERE county = %(county)s AND constituency = %(constituency)s AND name = %(name)s
    ''', candidate)
    r = c.fetchone()
    if r and not r[0]:
        print candidate['name']
        raw_input()


conn = db_settings.con()
c = conn.cursor()
election_year = '2014'
df = pd.read_csv('../../data/T1.csv', encoding='utf-8')
for row in df[df[u'是否現任'] == u'是'].iterrows():
    match = re.search(u'(?P<county>\S+)第(?P<constituency>.+)選(?:舉)?區', row[1][u'選舉區'])
    row[1]['name'] = row[1][u'姓名']
    row[1]['county'] = match.group('county')
    row[1]['constituency'] = match.group('constituency')
    row[1]['election_year'] = election_year
    in_office(row[1])
