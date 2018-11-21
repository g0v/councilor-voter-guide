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
sh = gc.open_by_key('1ZJkyZax00bjK9ffRPwzJRDsBBIgboyJfFA4TNuifTdA')
wks = sh.sheet1
rows = wks.get_all_records()
for candidate in rows:
    if not candidate[u'學歷'] and not candidate[u'經歷']:
        continue
    candidate['name'] = common.normalize_person_name(candidate['name'])
    print candidate['name']
    candidate['election_year'] = election_year
    candidate['education'] = candidate[u'學歷']
    candidate['experience'] = candidate[u'經歷']
    if int(candidate['constituency']) == 0:
        candidate['candidate_uid'], created = common.get_or_create_moyor_candidate_uid(c, candidate, create=False)
    else:
        candidate['candidate_uid'], created = common.get_or_create_candidate_uid(c, candidate, create=False)
    c.execute('''
        UPDATE candidates_terms
        SET education = E%(education)s, experience = E%(experience)s
        WHERE election_year = %(election_year)s AND candidate_id = %(candidate_uid)s
    ''', candidate)
conn.commit()
