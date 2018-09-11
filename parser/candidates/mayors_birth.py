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


def AD2DATE(text):
    matchTerm = re.search(u'''
        (?P<year>[\d]+)[\s]*(?:年|[-/.])[\s]*
        (?P<month>[\d]+)[\s]*(?:月|[-/.])[\s]*
        (?P<day>[\d]+)
    ''', text, re.X)
    if matchTerm:
        return '%04d-%02d-%02d' % (int(matchTerm.group('year')), int(matchTerm.group('month')), int(matchTerm.group('day')))
    matchTerm = re.search(u'''
        (?P<year>[\d]+)[\s]*(?:年|[-/.])[\s]*
        [\s]*(?:月|[-/.])[\s]*
    ''', text, re.X)
    if matchTerm:
        return '%04d-01-01' % (int(matchTerm.group('year')), )

def upsertCandidates(candidate):
    candidate['former_names'] = candidate.get('former_names', [])
    variants = common.make_variants_set(candidate['name'])
    candidate['identifiers'] = list((variants | set(candidate['former_names']) | {candidate['name'], re.sub(u'[\w‧]', '', candidate['name']), re.sub(u'\W', '', candidate['name']).lower(), }) - {''})
    complement = {'birth': None, 'gender': '', 'party': '', 'number': None, 'contact_details': None, 'district': '', 'education': None, 'experience': None, 'remark': None, 'image': '', 'links': None, 'platform': '', 'data': None, 'occupy': None}
    complement.update(candidate)
    c.execute('''
        UPDATE candidates_candidates
        SET birth = COALESCE(candidates_candidates.birth, %(birth)s)
        WHERE uid = %(candidate_uid)s
    ''', complement)

conn = db_settings.con()
c = conn.cursor()
election_year = '2018'

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credential.json', scope)
gc = gspread.authorize(credentials)
for key in ['1FdpMYYsyf9VlQapcf_ckhDDi_3zNXU044TE84-1hBx0', '1MfWFgLM23qjPkZWz2xv89_sFRRXdynrX9TnciPZajNk']:
    sh = gc.open_by_key(key)
    worksheets = sh.worksheets()
    for wks in worksheets:
        print wks.title
        rows = wks.get_all_records()
        position_type = 'mayors'
        county = wks.title.replace(u'台', u'臺')
        for row in rows:
            candidate = {}
            candidate['party'] = common.normalize_party(row[u'黨籍'])
            if not row[u'姓名']:
                continue
            candidate['type'] = position_type
            candidate['county'] = county
            candidate['constituency'] = 0
            candidate['name'] = common.normalize_person_name(row[u'姓名'])
            candidate['election_year'] = election_year
            candidate['birth'] = AD2DATE(row[u'出生年月日'])
            if position_type == 'mayors':
                candidate['candidate_uid'], created = common.get_or_create_moyor_candidate_uid(c, candidate)
            upsertCandidates(candidate)
conn.commit()
