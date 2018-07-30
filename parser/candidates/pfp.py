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


def upsertCandidates(candidate):
    candidate['former_names'] = candidate.get('former_names', [])
    variants = common.make_variants_set(candidate['name'])
    candidate['identifiers'] = list((variants | set(candidate['former_names']) | {candidate['name'], re.sub(u'[\w‧]', '', candidate['name']), re.sub(u'\W', '', candidate['name']).lower(), }) - {''})
    complement = {'birth': None, 'gender': '', 'party': '', 'number': None, 'contact_details': None, 'district': '', 'education': None, 'experience': None, 'remark': None, 'image': '', 'links': None, 'platform': '', 'data': None, 'occupy': None}
    complement.update(candidate)
    c.execute('''
        INSERT INTO candidates_candidates(uid, name, birth, identifiers)
        VALUES (%(candidate_uid)s, %(name)s, %(birth)s, %(identifiers)s)
        ON CONFLICT (uid)
        DO UPDATE
        SET name = %(name)s, birth = %(birth)s, identifiers = %(identifiers)s
    ''', complement)
    c.execute('''
        INSERT INTO candidates_terms(uid, candidate_id, elected_councilor_id, councilor_terms, election_year, number, name, gender, party, constituency, county, district, contact_details, education, experience, remark, image, links, platform, type, occupy)
        VALUES (%(candidate_term_uid)s, %(candidate_uid)s, %(councilor_term_id)s, %(councilor_terms)s, %(election_year)s, %(number)s, %(name)s, %(gender)s, %(party)s, %(constituency)s, %(county)s, %(district)s, %(contact_details)s, %(education)s, %(experience)s, %(remark)s, %(image)s, %(links)s, %(platform)s, %(type)s, %(occupy)s)
        ON CONFLICT (election_year, candidate_id)
        DO UPDATE
        SET elected_councilor_id = %(councilor_term_id)s, councilor_terms = %(councilor_terms)s, number = %(number)s, name = %(name)s, gender = %(gender)s, party = %(party)s, constituency = %(constituency)s, county = %(county)s, district = %(district)s, contact_details = %(contact_details)s, education = %(education)s, experience = %(experience)s, remark = %(remark)s, image = %(image)s, links = %(links)s, occupy = %(occupy)s
    ''', complement)
    terms = []
    for t in ['mayor', 'legislator', 'councilor']:
        if candidate.get('%s_terms' % t):
            for term in candidate['%s_terms' % t]:
                term['type'] = t
                terms.append(term)
    c.execute('''
        UPDATE candidates_terms
        SET data = (COALESCE(data, '{}'::jsonb) || %s::jsonb)
        WHERE election_year = %s and candidate_id = %s
    ''', [json.dumps({'terms': terms}), complement['election_year'], complement['candidate_uid'], ])
    if candidate.get('mayor_terms'):
        c.execute('''
            UPDATE candidates_terms
            SET data = (COALESCE(data, '{}'::jsonb) || %s::jsonb)
            WHERE election_year = %s and candidate_id = %s
        ''', [json.dumps({'mayor_terms': complement['mayor_terms']}), complement['election_year'], complement['candidate_uid'], ])
    if candidate.get('legislator_terms'):
        c.execute('''
            UPDATE candidates_terms
            SET data = (COALESCE(data, '{}'::jsonb) || %s::jsonb)
            WHERE election_year = %s and candidate_id = %s
        ''', [json.dumps({'legislator_terms': complement['legislator_terms']}), complement['election_year'], complement['candidate_uid'], ])
    if candidate.get('legislator_data'):
        c.execute('''
            UPDATE candidates_terms
            SET data = (COALESCE(data, '{}'::jsonb) || %s::jsonb)
            WHERE election_year = %s and candidate_id = %s
        ''', [json.dumps({'legislator_data': complement['legislator_data']}), complement['election_year'], complement['candidate_uid'], ])
    if candidate.get('legislator_candidate_info'):
        c.execute('''
            UPDATE candidates_terms
            SET politicalcontributions = COALESCE(politicalcontributions, '[]'::jsonb) || %s::jsonb
            WHERE election_year >= %s and candidate_id = %s
        ''', [candidate['legislator_candidate_info']['politicalcontributions'], complement['election_year'], complement['candidate_uid'], ])
        c.execute('''
            UPDATE candidates_terms
            SET politicalcontributions = (SELECT jsonb_agg(x) FROM (
                SELECT x from (
                    SELECT DISTINCT(value) as x
                    FROM jsonb_array_elements(politicalcontributions)
                ) t ORDER BY x->'election_year' DESC
            ) tt)
            WHERE candidate_id = %s AND election_year >= %s
        ''', [complement['candidate_uid'], complement['election_year'], ])

conn = db_settings.con()
conn_another = db_settings.con_another()
c = conn.cursor()
c_another = conn_another.cursor()
election_year = '2018'
party = u'親民黨'

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credential.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_key('1mfxUMjmEUnFN8bSlDaveZiGxUSQTgCGXCB-YkZtN8uc')
worksheets = sh.worksheets()
for wks in worksheets:
    rows = wks.get_all_records()
    position_type = 'councilors'
    path = '../../data/avatar/%s/%s/%s' % (position_type, election_year, party)
    for row in rows:
        if not row[u'姓名'] or not row[u'選區號次(EX:5)']:
            continue
        candidate = {}
        candidate['type'] = position_type
        candidate['county'] = re.search(u'(\W+[縣市])', row[u'選區縣市']).group().replace(u'台', u'臺')
        candidate['constituency'] = row[u'選區號次(EX:5)']
        candidate['name'] = common.normalize_person_name(row[u'姓名'])
        candidate['party'] = party
        candidate['election_year'] = election_year
        candidate['birth'] = row[u'生日(yyyy-mm-dd)'] or None
        candidate['gender'] = row[u'性別']
        candidate['education'] = row[u'學歷']
        candidate['experience'] = row[u'經歷']
        if candidate['type'] == 'mayors':
            candidate['candidate_uid'], created = common.get_or_create_moyor_candidate_uid(c, candidate)
        else:
            candidate['candidate_uid'], created = common.get_or_create_candidate_uid(c, candidate)
        candidate['candidate_term_uid'] = '%s-%s' % (candidate['candidate_uid'], election_year)
        candidate['councilor_uid'], created = common.get_or_create_councilor_uid(c, candidate, create=False)
        candidate['councilor_term_id'] = common.getDetailIdFromUid(c, candidate['councilor_uid'], election_year, candidate['county'])
        candidate['councilor_terms'] = common.councilor_terms(c, candidate) if created else None
        if candidate['type'] == 'mayors':
            candidate['mayor_uid'] = candidate['candidate_uid']
            if candidate['mayor_uid']:
                candidate['mayor_terms'] = common.mayor_terms(c, candidate)
            candidate['legislator_uid'] = common.get_legislator_uid(c_another, candidate['name'])
            candidate['legislator_data'] = common.get_legislator_data(c_another, candidate['legislator_uid'])
            if candidate['legislator_uid']:
                candidate['legislator_terms'] = common.legislator_terms(c_another, candidate)
                candidate['legislator_candidate_info'] = common.get_elected_legislator_candidate_info(c_another, candidate)
                if candidate['legislator_candidate_info']:
                    candidate['birth'] = candidate['legislator_candidate_info']['birth']
            candidate['occupy'] = common.is_mayor_occupy(c, candidate)
        else:
            candidate['occupy'] = common.is_councilor_occupy(c, candidate)
        upsertCandidates(candidate)
conn.commit()
