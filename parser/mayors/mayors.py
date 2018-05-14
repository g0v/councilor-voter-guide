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

def upsert_mayors(mayor):
    mayor['former_names'] = mayor.get('former_names', [])
    variants = common.make_variants_set(mayor['name'])
    mayor['identifiers'] = list((variants | set(mayor['former_names']) | {mayor['name'], re.sub(u'[\w‧]', '', mayor['name']), re.sub(u'\W', '', mayor['name']).lower(), }) - {''})
    complement = {"birth": None}
    complement.update(mayor)
    c.execute('''
        INSERT INTO mayors_mayors(uid, name, birth, identifiers)
        VALUES (%(uid)s, %(name)s, %(birth)s, %(identifiers)s)
        ON CONFLICT (uid)
        DO UPDATE
        SET name = %(name)s, birth = %(birth)s, identifiers = %(identifiers)s
    ''', complement)

def upsert_mayors_terms(mayor):
    for key in ['education', 'experience', 'platform', 'remark']:
        if mayor.has_key(key) and type(mayor[key]) is list:
            mayor[key] = '\n'.join(mayor[key])
    complement = {"gender": '', "party": '', "contact_details": None, "county": '', "in_office": True, "term_start": None, "term_end": {}, "education": None, "experience": None, "remark": None, "image": '', "links": None, "platform": ''}
    complement.update(mayor)
    c.execute('''
        INSERT INTO mayors_terms(uid, mayor_id, election_year, name, gender, party, county, in_office, contact_details, term_start, term_end, education, experience, remark, image, links, platform)
        VALUES (%(term_uid)s, %(uid)s, %(election_year)s, %(name)s, %(gender)s, %(party)s, %(county)s, %(in_office)s, %(contact_details)s, %(term_start)s, %(term_end)s, %(education)s, %(experience)s, %(remark)s, %(image)s, %(links)s, %(platform)s)
        ON CONFLICT (mayor_id, election_year)
        DO UPDATE
        SET name = %(name)s, gender = %(gender)s, party = %(party)s, in_office = %(in_office)s, contact_details = %(contact_details)s, county = %(county)s, term_start = %(term_start)s, term_end = %(term_end)s, education = %(education)s, experience = %(experience)s, remark = %(remark)s, image = %(image)s, links = %(links)s, platform = %(platform)s
    ''', complement)

conn = db_settings.con()
c = conn.cursor()

# insert mayors which elected=true in candidates
election_year = ast.literal_eval(argv[1])['election_year']
c.execute('''
    SELECT ct.*, c.birth
    FROM candidates_terms ct
    Join candidates_candidates c ON c.uid = ct.candidate_id
    WHERE type = 'mayors' and election_year = %s and elected = true
''', [election_year])
key = [desc[0] for desc in c.description]
for row in c.fetchall():
    person = dict(zip(key, row))
    person['uid'] = person['candidate_id']
    person['term_uid'] = '%s-%s' % (person['uid'], person['election_year'])
    person['name'] = person['name'].decode('utf-8')
    person['in_office'] = True
    person['term_start'] = {'2009': '2009-12-20', '2010': '2010-12-25', '2014': '2014-12-25'}[person['election_year']]
    person['term_end'] = {
        'date': {'2009': '2014-12-25', '2010': '2014-12-25', '2014': '2018-12-25'}[person['election_year']]
    }
    upsert_mayors(person)
    upsert_mayors_terms(person)
conn.commit()
