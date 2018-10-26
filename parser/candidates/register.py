#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import ast
from sys import argv

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
        SET name = %(name)s, birth = COALESCE(candidates_candidates.birth, %(birth)s), identifiers = %(identifiers)s
    ''', complement)
    c.execute('''
        INSERT INTO candidates_terms(uid, candidate_id, elected_councilor_id, councilor_terms, election_year, number, name, party, constituency, county, type, occupy, status)
        VALUES (%(candidate_term_uid)s, %(candidate_uid)s, %(councilor_term_id)s, %(councilor_terms)s, %(election_year)s, %(number)s, %(name)s, %(party)s, %(constituency)s, %(county)s, %(type)s, %(occupy)s, %(status)s)
        ON CONFLICT (election_year, candidate_id)
        DO UPDATE
        SET elected_councilor_id = %(councilor_term_id)s, councilor_terms = %(councilor_terms)s, number = %(number)s, name = %(name)s, party = %(party)s, constituency = %(constituency)s, county = %(county)s, type = %(type)s, occupy = %(occupy)s, status = %(status)s, image = COALESCE(candidates_terms.image, %(image)s)
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
                    WHERE value->'title' is not null
                ) t ORDER BY x->'election_year' DESC
            ) tt)
            WHERE candidate_id = %s AND election_year >= %s
        ''', [complement['candidate_uid'], complement['election_year'], ])

conn = db_settings.con()
conn_another = db_settings.con_another()
c = conn.cursor()
c_another = conn_another.cursor()
election_year = '2018'
target_county = ast.literal_eval(argv[1])['county'] if len(argv) > 1 else None

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credential.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_key('1LMiLY8I-mpVL0AHWlOTSqpurzpgCHjrvi8qJDQkfreY')
worksheets = sh.worksheets()
for wks in worksheets:
    rows = wks.get_all_records()
    if re.search(u'議員', wks.title):
        position_type = 'councilors'
    elif re.search(u'市長', wks.title):
        position_type = 'mayors'
    else:
        continue
    for row in rows:
        if not row[u'姓名'] or row[u'姓名'] == u'姓名':
            continue
        candidate = {}
        candidate['type'] = position_type
        candidate['status'] = 'register'
        if candidate['type'] == 'councilors':
            match = re.search(u'(?P<county>\W+)第(?P<num>\d+)選(?:舉)?區', row[u'選舉區'])
            candidate['county'] = match.group('county') if match else None
            candidate['constituency'] = match.group('num') if match else None
        else:
            candidate['county'] = row[u'選舉區']
            candidate['constituency'] = 0
        if target_county and candidate['county'].encode('utf-8') != target_county:
            continue
        candidate['name'] = common.normalize_person_name(row[u'姓名'])
        print candidate['name'], candidate['county'], candidate['constituency']
        candidate['party'] = common.normalize_party(row[u'推薦之政黨'])
        candidate['election_year'] = election_year
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
                candidate['legislator_candidate_info'] = common.get_legislator_candidate_info(c_another, candidate['name'])
                if candidate['legislator_candidate_info']:
                    candidate['birth'] = candidate['legislator_candidate_info']['birth']
            candidate['occupy'] = common.is_mayor_occupy(c, candidate)
            if candidate['occupy']:
                candidate['image'] = common.mayor_image(c, candidate)
        else:
            candidate['occupy'] = common.is_councilor_occupy(c, candidate)
            if candidate['occupy']:
                candidate['image'] = common.councilor_image(c, candidate)
        upsertCandidates(candidate)
conn.commit()
