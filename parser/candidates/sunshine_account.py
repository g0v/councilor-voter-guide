#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import json
import glob
import psycopg2
from datetime import datetime
import pandas as pd
import ast
from sys import argv

import db_settings
import common


def upsertCandidates(candidate):
    candidate['former_names'] = candidate.get('former_names', [])
    variants = common.make_variants_set(candidate['name'])
    candidate['identifiers'] = list((variants | set(candidate['former_names']) | {candidate['name'], re.sub(u'[\w‧]', '', candidate['name']), re.sub(u'\W', '', candidate['name']).lower(), }) - {''})
    complement = {'birth': None, 'gender': '', 'party': '', 'number': None, 'contact_details': None, 'district': '', 'education': None, 'experience': None, 'remark': None, 'image': '', 'links': None, 'platform': '', 'data': None}
    complement.update(candidate)
    c.execute('''
        INSERT INTO candidates_candidates(uid, name, birth, identifiers)
        VALUES (%(candidate_uid)s, %(name)s, %(birth)s, %(identifiers)s)
        ON CONFLICT (uid)
        DO UPDATE
        SET name = %(name)s, birth = %(birth)s, identifiers = %(identifiers)s
    ''', complement)
    c.execute('''
        INSERT INTO candidates_terms(uid, candidate_id, elected_councilor_id, councilor_terms, election_year, number, name, gender, party, constituency, county, district, contact_details, education, experience, remark, image, links, platform, type)
        VALUES (%(candidate_term_uid)s, %(candidate_uid)s, %(councilor_term_id)s, %(councilor_terms)s, %(election_year)s, %(number)s, %(name)s, %(gender)s, %(party)s, %(constituency)s, %(county)s, %(district)s, %(contact_details)s, %(education)s, %(experience)s, %(remark)s, %(image)s, %(links)s, %(platform)s, %(type)s)
        ON CONFLICT (election_year, candidate_id)
        DO UPDATE
        SET elected_councilor_id = %(councilor_term_id)s, councilor_terms = %(councilor_terms)s, number = %(number)s, name = %(name)s, gender = %(gender)s, party = %(party)s, constituency = %(constituency)s, county = %(county)s, district = %(district)s, contact_details = %(contact_details)s, education = %(education)s, experience = %(experience)s, remark = %(remark)s, image = %(image)s, links = %(links)s
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
election_year = ast.literal_eval(argv[1])['election_year']
df = pd.read_csv('../../data/candidates/%s/sunshine_account.csv' % election_year, encoding='utf-8', usecols=[0, 1], header=None)
for row in df.iterrows():
    if not row[0]:
        continue
    candidate = {}
    candidate['type'] = 'councilors' if re.search(u'議員', row[1]) else 'mayors'
    candidate['county'] = re.search(u'年(\W+[縣市])'].group()
    candidate['name'] = common.normalize_person_name(row[0])
    candidate['election_year'] = election_year
    if candidate['type'] = 'councilors':
        candidate['constituency'] = int(match.group('num'))
    else:
        candidate['constituency'] = 0
    if position_type == 'mayors':
        candidate['candidate_uid'], created = common.get_or_create_moyor_candidate_uid(c, candidate)
    else:
        candidate['candidate_uid'], created = common.get_or_create_candidate_uid(c, candidate)
    candidate['candidate_term_uid'] = '%s-%s' % (candidate['candidate_uid'], election_year)
    candidate['councilor_uid'], created = common.get_or_create_councilor_uid(c, candidate, create=False)
    candidate['councilor_term_id'] = common.getDetailIdFromUid(c, candidate['councilor_uid'], election_year, candidate['county'])
    candidate['councilor_terms'] = common.councilor_terms(c, candidate) if created else None
    if position_type == 'mayors':
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
    upsertCandidates(candidate)
#conn.commit()
