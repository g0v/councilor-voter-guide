#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import json
import glob
import psycopg2
from datetime import datetime
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
        INSERT INTO candidates_terms(uid, candidate_id, type, election_year, number, name, gender, party, constituency, county, district, contact_details, education, experience, remark, image, links, platform, votes, votes_percentage, votes_detail, elected, occupy)
        VALUES (%(candidate_term_uid)s, %(candidate_uid)s, %(type)s, %(election_year)s, %(number)s, %(name)s, %(gender)s, %(party)s, %(constituency)s, %(county)s, %(district)s, %(contact_details)s, %(education)s, %(experience)s, %(remark)s, %(image)s, %(links)s, %(platform)s, %(votes)s, %(votes_percentage)s, %(votes_detail)s, %(elected)s, %(occupy)s)
        ON CONFLICT (election_year, candidate_id)
        DO UPDATE
        SET type = %(type)s, number = %(number)s, name = %(name)s, gender = %(gender)s, party = %(party)s, constituency = %(constituency)s, county = %(county)s, district = %(district)s, contact_details = %(contact_details)s, education = %(education)s, experience = %(experience)s, remark = %(remark)s, image = %(image)s, links = %(links)s, votes = %(votes)s, votes_percentage = %(votes_percentage)s, votes_detail = %(votes_detail)s, elected = %(elected)s, occupy = %(occupy)s
    ''', complement)

conn = db_settings.con()
c = conn.cursor()
election_year = ast.literal_eval(argv[1])['election_year']
county_versions = json.load(open('../county_versions.json'))
candidates = json.load(open('../../data/candidates/%s/mayors.json' % election_year))
for candidate in candidates:
    candidate['type'] = 'mayors'
    candidate['elected'] = True if re.search(u'[*!]', candidate['elected']) else False
    candidate['occupy'] = True if re.search(u'是', candidate['occupy']) else False
    candidate['district'] = candidate['county']
    candidate['constituency'] = 0
    candidate['birth'] = candidate['birth_year']
    candidate['birth'] = datetime.strptime(str(candidate['birth']), '%Y')
    for county_change in county_versions.get(election_year, []):
        candidate['previous_county'] = county_change['from'] if candidate['county'] == county_change['to'] else candidate['county']
    candidate['name'] = common.normalize_person_name(candidate['name'])
    candidate['party'] = common.normalize_party(candidate['party'])
    candidate['election_year'] = election_year
    candidate['candidate_uid'], created = common.get_or_create_moyor_candidate_uid(c, candidate)
    candidate['candidate_term_uid'] = '%s-%s' % (candidate['candidate_uid'], election_year)
    upsertCandidates(candidate)
conn.commit()
