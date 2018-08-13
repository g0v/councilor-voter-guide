#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
import uuid
import json
import glob
import codecs
from datetime import datetime
import ast
from sys import argv

import pandas as pd

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
        INSERT INTO candidates_terms(uid, candidate_id, type, election_year, number, name, gender, party, constituency, county, district, votes, votes_percentage, votes_detail, elected, occupy)
        VALUES (%(candidate_term_uid)s, %(candidate_uid)s, %(type)s, %(election_year)s, %(number)s, %(name)s, %(gender)s, %(party)s, %(constituency)s, %(county)s, %(district)s, %(votes)s, %(votes_percentage)s, %(votes_detail)s, %(elected)s, %(occupy)s)
        ON CONFLICT (election_year, candidate_id)
        DO UPDATE
        SET type = %(type)s, number = %(number)s, name = %(name)s, gender = %(gender)s, party = %(party)s, constituency = %(constituency)s, county = %(county)s, district = %(district)s, votes = %(votes)s, votes_percentage = %(votes_percentage)s, votes_detail = %(votes_detail)s, elected = %(elected)s, occupy = %(occupy)s
    ''', complement)

conn = db_settings.con()
c = conn.cursor()
election_year = ast.literal_eval(argv[1])['election_year']
county_versions = json.load(open('../county_versions.json'))
candidates = json.load(open('../../data/candidates/%s/councilors.json' % election_year))
for candidate in candidates:
    if not candidate['name']:
        continue
    candidate['type'] = 'councilors'
    candidate['elected'] = True if re.search(u'[*!]', candidate['elected'] or '') else False
    candidate['occupy'] = True if re.search(u'是', candidate['occupy']) else False
    constituency = re.sub('\D', '', candidate['county'])
    print candidate['name'], candidate['county']
    if constituency:
        candidate['constituency'] = int(re.sub('\D', '', candidate['county']))
    else:
        constituency = common.normalize_constituency(candidate['county'])
        if constituency:
            candidate['constituency'] = constituency
        elif candidate['votes_detail']:
            print candidate['votes_detail']
            constituency = re.sub('\D', '', candidate['votes_detail'][0]['district'])
            if constituency:
                candidate['constituency'] = int(constituency)
    candidate['county'] = re.search(u'(.+?[縣市])', candidate['county']).group(1)
    if candidate['category'] == u'區域':
        candidate['district'] = u'、'.join([re.sub(u'.+選區', '', x['district']) for x in candidate['votes_detail']])
    elif candidate['category'] == u'原住民':
        candidate['district'] = u'原住民'
        if candidate['county'] == u'臺北市':
            candidate['constituency'] = 7
        elif candidate['county'] == u'高雄市':
            candidate['constituency'] = 6
    else:
        candidate['district'] = u'%s原住民' % candidate['category']
    candidate['birth'] = candidate['birth_year']
    candidate['birth'] = datetime.strptime(str(candidate['birth']), '%Y')
    for county_change in county_versions.get(election_year, []):
        candidate['previous_county'] = county_change['from'] if candidate['county'] == county_change['to'] else candidate['county']
    candidate['name'] = common.normalize_person_name(candidate['name'])
    candidate['party'] = common.normalize_party(candidate['party'])
    candidate['election_year'] = election_year
    candidate['candidate_uid'], created = common.get_or_create_candidate_uid(c, candidate)
    candidate['candidate_term_uid'] = '%s-%s' % (candidate['candidate_uid'], election_year)
    upsertCandidates(candidate)
conn.commit()

# generate constituencies_yyyy.json
c.execute('''
    SELECT jsonb_agg(_)
    FROM (
        SELECT county, constituency, district
        FROM candidates_terms ct
        WHERE type = 'councilors' and election_year = %s and district != ''
        GROUP BY county, constituency, district
        ORDER BY county, constituency, district
    ) _
''', [election_year])
rows = c.fetchone()
f_out = '../../voter_guide/static/json/dest/constituencies_%s.json' % election_year
json.dump(rows[0], codecs.open(f_out, 'w', 'utf-8'), ensure_ascii=False)
