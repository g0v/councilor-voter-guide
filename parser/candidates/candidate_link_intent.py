#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import db_settings
import common


conn = db_settings.con()
c = conn.cursor()
election_year = '2018'

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credential.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_key('1URc-N8UnptWv0h7P1Aciar4NZgetWK7boVC6zrwQ3Iw')
wks = sh.sheet1
rows = wks.get_all_records()
for candidate in rows:
    if not candidate['status']:
        continue
    candidate['name'] = common.normalize_person_name(candidate['user_input_name'])
    print candidate['name']
    candidate['election_year'] = election_year
    if candidate['type'] == 'mayors':
        candidate['candidate_uid'], created = common.get_or_create_moyor_candidate_uid(c, candidate, create=False)
    else:
        candidate['candidate_uid'], created = common.get_or_create_candidate_uid(c, candidate, create=False)
    if candidate['candidate_uid']:
        candidate['candidate_term_uid'] = '%s-%s' % (candidate['candidate_uid'], election_year)
    else:
        continue
    c.execute('''
        SELECT 1
        FROM candidates_terms
        WHERE election_year = %s and uid = %s
    ''', [election_year, candidate['candidate_term_uid']])
    r = c.fetchone()
    if r and r[0]:
        c.execute('''
            UPDATE candidates_intent
            SET candidate_id = %(candidate_uid)s, candidate_term_id = %(candidate_term_uid)s
            WHERE type = %(type)s AND election_year = %(election_year)s AND uid = %(uid)s
        ''', candidate)
conn.commit()
