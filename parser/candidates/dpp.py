#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import db_settings
import common


def councilor_terms(candidate):
    '''
    Parse working recoed before the election_year of this candidate into a json to store in individual candidate, so we could display councilor's working records easier at candidate page(no need of a lot of reference).
    '''

    c.execute('''
        SELECT id as term_id, councilor_id, election_year, param, to_char(EXTRACT(YEAR FROM term_start), '9999') as term_start_year, substring(term_end->>'date' from '(\d+)-') as term_end_year
        FROM councilors_councilorsdetail
        WHERE councilor_id = %(councilor_uid)s AND election_year <= %(election_year)s
        ORDER BY election_year DESC
    ''', candidate)
    key = [desc[0] for desc in c.description]
    terms = []
    r = c.fetchall()
    for row in r:
        terms.append(dict(zip(key, row)))
    return terms

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

conn = db_settings.con()
c = conn.cursor()
election_year = '2018'
party = u'民主進步黨'

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credential.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_key('1efxsRJKSoezKVJvln2rNkl-nGIZlmngw6k35GgKxLAE')
worksheets = sh.worksheets()
for wks in worksheets:
    rows = wks.get_all_records()
    position_type = 'councilors' if wks.title == u'議員' else 'mayors'
    for row in rows:
        if not row[u'姓名']:
            continue
        candidate = {}
        candidate['type'] = position_type
        candidate['county'] = row[u'參選縣市'].replace(u'台', u'臺')
        if row.get(u'選區'):
            match = re.search(u'第(?P<num>\d+)選(?:舉)?區', row[u'選區'])
            candidate['constituency'] = int(match.group('num'))
        else:
            candidate['constituency'] = 0
        candidate['name'] = common.normalize_person_name(row[u'姓名'])
        candidate['party'] = party
        candidate['election_year'] = election_year
        candidate['gender'] = row[u'性別']
        candidate['education'] = row[u'學歷']
        candidate['experience'] = row[u'經歷']
        if row[u'相關連結']:
            if re.search('facebook', row[u'相關連結']):
                candidate['links'] = [{'url': row[u'相關連結'], 'note': 'facebook'}]
            else:
                candidate['links'] = [{'url': row[u'相關連結'], 'note': u'相關連結'}]
        if row[u'照片有無']:
            candidate['image'] = u'%s/%s/%s/%s/%s' % (common.storage_domain(), position_type, election_year, party, row[u'照片有無'])
        candidate['candidate_uid'], created = common.get_or_create_candidate_uid(c, candidate)
        candidate['candidate_term_uid'] = '%s-%s' % (candidate['candidate_uid'], election_year)
        candidate['councilor_uid'], created = common.get_or_create_councilor_uid(c, candidate)
        candidate['councilor_term_id'] = common.getDetailIdFromUid(c, candidate['councilor_uid'], election_year, candidate['county'])

        candidate['councilor_terms'] = councilor_terms(candidate) if created else None
        upsertCandidates(candidate)
conn.commit()
