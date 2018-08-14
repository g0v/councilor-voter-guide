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
c = conn.cursor()
election_year = '2018'
district_versions = json.load(open('../district_versions.json'))

c.execute('''
    SELECT row_to_json(_)
    FROM (
        SELECT c.*, COALESCE(t.image, c.image) as image
        FROM councilors_councilorsdetail c
        LEFT JOIN candidates_terms t ON t.elected_councilor_id = c.id
        WHERE c.in_office = true AND c.party not in ('中國國民黨', '民主進步黨', '時代力量', '親民黨') AND c.election_year in %s
    ) _
''', [tuple(common.last_election_years(election_year))])
rows = c.fetchall()
position_type = 'councilors'
for row in rows:
    candidate = row[0]
    print candidate['name'], candidate['election_year'], candidate['party']
    candidate['type'] = position_type
    candidate['election_year'] = election_year
    for district_change in reversed(district_versions[election_year].get(candidate['county'], [])):
        if str(candidate['constituency']) in district_change.get('from', {}).get('constituencies', []):
            candidate['district'] = district_change['district']
            candidate['constituency'] = district_change['constituency']
            break
    candidate['candidate_uid'], created = common.get_or_create_candidate_uid(c, candidate)
    candidate['candidate_term_uid'] = '%s-%s' % (candidate['candidate_uid'], election_year)
    candidate['councilor_uid'], created = common.get_or_create_councilor_uid(c, candidate, create=False)
    candidate['councilor_term_id'] = common.getDetailIdFromUid(c, candidate['councilor_uid'], election_year, candidate['county'])
    candidate['councilor_terms'] = common.councilor_terms(c, candidate) if created else None
    candidate['occupy'] = True
    upsertCandidates(candidate)
conn.commit()
