#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
import json
import uuid
import codecs
import logging
import ast
from sys import argv

import db_settings
import common


logging.basicConfig(filename='parser.log', level=logging.ERROR)

def upsert_councilors(councilor):
    councilor['former_names'] = councilor.get('former_names', [])
    variants = common.make_variants_set(councilor['name'])
    councilor['identifiers'] = list((variants | set(councilor['former_names']) | {councilor['name'], re.sub(u'[\w‧]', '', councilor['name']), re.sub(u'\W', '', councilor['name']).lower(), }) - {''})
    councilor['former_names'] = '\n'.join(councilor['former_names'])
    complement = {"birth": None}
    complement.update(councilor)
    c.execute('''
        INSERT INTO councilors_councilors(uid, name, birth, former_names, identifiers)
        VALUES (%(uid)s, %(name)s, %(birth)s, %(former_names)s, %(identifiers)s)
        ON CONFLICT (uid)
        DO UPDATE
        SET name = %(name)s, birth = %(birth)s, former_names = %(former_names)s, identifiers = %(identifiers)s
    ''', complement)

def upsert_councilors_terms(councilor):
    for key in ['education', 'experience', 'platform', 'remark']:
        if councilor.has_key(key) and type(councilor[key]) is list:
            councilor[key] = '\n'.join(councilor[key])
    complement = {"gender": '', "party": '', "contact_details": None, "title": u'議員', "constituency": None, "county": '', "district": '', "in_office": True, "term_start": None, "term_end": {}, "education": None, "experience": None, "remark": None, "image": '', "links": None, "platform": ''}
    complement.update(councilor)
    c.execute('''
        INSERT INTO councilors_councilorsdetail(councilor_id, election_year, name, gender, party, title, constituency, county, district, in_office, contact_details, term_start, term_end, education, experience, remark, image, links, platform)
        VALUES (%(uid)s, %(election_year)s, %(name)s, %(gender)s, %(party)s, %(title)s, %(constituency)s, %(county)s, %(district)s, %(in_office)s, %(contact_details)s, %(term_start)s, %(term_end)s, %(education)s, %(experience)s, %(remark)s, %(image)s, %(links)s, %(platform)s)
        ON CONFLICT (councilor_id, election_year)
        DO UPDATE
        SET county = %(county)s, district = %(district)s
        RETURNING id
    ''', complement)
    r = c.fetchone()
    councilor_id = r[0]
    c.execute('''
        UPDATE candidates_terms
        SET elected_councilor_id = %s
        WHERE candidate_id = %s and election_year = %s
    ''', [councilor_id, councilor['candidate_id'], councilor['election_year']])

conn = db_settings.con()
c = conn.cursor()

# insert councilors which elected=true in candidates
election_year = ast.literal_eval(argv[1])['election_year']
c.execute('''
    SELECT json_agg(_)
    FROM (
        SELECT ct.*, c.birth
        FROM candidates_terms ct
        Join candidates_candidates c ON c.uid = ct.candidate_id
        WHERE type = 'councilors' and election_year = %s and elected = true
    ) _
''', [election_year])
for person in c.fetchone()[0]:
    print person['name'], person['county'], person['election_year']
    person['uid'], created = common.get_or_create_councilor_uid(c, person)
    person['uid'] = uuid.UUID(person['uid']).hex
    person['in_office'] = True
    person['term_start'], person['term_end'] = common.get_term_range(person['county'], person['election_year'])
    person['term_end'] = {'date': person['term_end']}
    upsert_councilors(person)
    upsert_councilors_terms(person)
conn.commit()
