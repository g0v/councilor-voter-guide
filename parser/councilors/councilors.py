#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
import json
import uuid
import codecs
import psycopg2
from psycopg2.extras import Json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging

import db_settings
import common


logging.basicConfig(filename='parser.log', level=logging.ERROR)

def get_constituency(councilor):
    if councilor.get('constituency'):
        return councilor['constituency']
    try:
        for k, v in constituency_maps[councilor['county']][councilor['election_year']].iteritems():
            if v == councilor['district']:
                return k
    except:
        pass
    return ''

def normalize_constituency(constituency):
    try:
        return int(constituency)
    except:
        pass
    match = re.search(u'第(?P<num>.+)選(?:舉)?區', constituency)
    if not match:
        return None
    try:
        return int(match.group('num'))
    except:
        logging.info(match.group('num'))
    ref = {u'一': 1, u'二': 2, u'三': 3, u'四': 4, u'五': 5, u'六': 6, u'七': 7, u'八': 8, u'九': 9}
    if re.search(u'^\s*十\s*$', match.group('num')):
        return 10
    num = re.sub(u'^\s*十', u'一', match.group('num'))
    num = re.sub(u'十', '', num)
    digits = re.findall(u'(一|二|三|四|五|六|七|八|九)', num)
    total, dec = 0, 1
    for i in reversed(range(0, len(digits))):
        total = total + int(ref.get(digits[i], 0)) * dec
        dec = dec * 10
    return total

def normalize_councilor(councilor):
    councilor['name'] = common.normalize_person_name(councilor['name'])
    councilor['name'] = re.sub(u'(副?議長|議員)', '', councilor['name'])
    councilor['gender'] = re.sub(u'性', '', councilor.get('gender', ''))
    if councilor.get('party'):
        councilor['party'] = common.normalize_party(councilor['party'])
    councilor['constituency'] = get_constituency(councilor)
    councilor['constituency'] = normalize_constituency(councilor['constituency'])
    return councilor

def Councilors(councilor):
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

def insertCouncilorsDetail(councilor):
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
        SET name = %(name)s, gender = %(gender)s, party = %(party)s, title = %(title)s, constituency = %(constituency)s, in_office = %(in_office)s, contact_details = %(contact_details)s, county = %(county)s, district = %(district)s, term_start = %(term_start)s, term_end = %(term_end)s, education = %(education)s, experience = %(experience)s, remark = %(remark)s, image = %(image)s, links = %(links)s, platform = %(platform)s
    ''', complement)

def examinate_with_cand_moi(councilor):
    matched = [person for person in merged_cand_moi
        if person['cityname'] == councilor['county'] and re.sub(u'[\s　]', '', person['idname']) == councilor['name']]
    if len(matched) > 1:
        logging.error(u'matched more than one of: %s, %s' % (councilor['county'], councilor['name']))
    elif len(matched) == 0:
        logging.error(u'no matched of: %s, %s' % (councilor['county'], councilor['name']))

with open(os.path.join(os.path.dirname(__file__), '../../data/cand-moi-county-control-2018.json'), 'r') as infile:
    merged_cand_moi = json.loads(infile.read())
with open(os.path.join(os.path.dirname(__file__), '../../data/cand-moi-direct-control-2018.json'), 'r') as infile:
    direct_control = json.loads(infile.read())
merged_cand_moi.extend(direct_control)
conn = db_settings.con()
c = conn.cursor()
constituency_maps = json.load(open('../constituency.json'))

# update all councilor's identifiers
c.execute('''
    SELECT *
    FROM councilors_councilors
''')
key = [desc[0] for desc in c.description]
for row in c.fetchall():
    person = dict(zip(key, row))
    person['name'] = person['name'].decode('utf-8')
    person['name'] = common.normalize_person_name(person['name'])
    Councilors(person)
conn.commit()

# upsert from json
for council in ['../../data/phcouncil/councilors.json', '../../data/kmcc/councilors.json', '../../data/mtcc/councilors.json', '../../data/ptcc/councilors.json', '../../data/kcc/councilors.json', '../../data/tncc/councilors.json', '../../data/taitungcc/councilors.json', '../../data/hlcc/councilors.json', '../../data/cycc/councilors.json', '../../data/cyscc/councilors.json', '../../data/ylcc/councilors.json', '../../data/ntcc/councilors.json', '../../data/chcc/councilors.json', '../../data/tccc/councilors.json', '../../data/ilcc/councilors.json', '../../data/mcc/councilors.json', '../../data/hcc/councilors.json', '../../data/kmc/councilors.json', '../../data/tycc/councilors.json', '../../data/hsinchucc/councilors.json', '../../data/ntp/councilors.json', '../../data/tcc/councilors.json']:
    print council
    dict_list = json.load(open(council))
    for councilor in dict_list:
        councilor = normalize_councilor(councilor)
        councilor['uid'], created = common.get_or_create_councilor_uid(c, councilor)
        Councilors(councilor)
        insertCouncilorsDetail(councilor)
        if councilor['in_office']:
            examinate_with_cand_moi(councilor)
conn.commit()

# insert councilor which elected=true in candidates but already gone in councils website
election_year = '2014'
c.execute('''
    SELECT *
    FROM candidates_terms
    WHERE election_year = %s and elected = true
    ORDER BY county
''', [election_year])
key = [desc[0] for desc in c.description]
for row in c.fetchall():
    person = dict(zip(key, row))
    person['name'] = person['name'].decode('utf-8')
    person = normalize_councilor(person)
    person['in_office'] = False
    councilor_ids = common.GetCouncilorId(c, person['name'])
    if not councilor_ids: # 完全沒出現過
        person['uid'] = uuid.uuid4().hex
        Councilors(person)
        insertCouncilorsDetail(person)
        continue
    else: # 出現過，但該屆還沒有資料的需 insert
        person['uid'], created = common.get_or_create_councilor_uid(c, person)
        if not created:
            logging.error(u'exist in councilor but not exist in councilordetail: %s, %s' % (person['county'], person['name'], person['']))
            continue
        if len(councilor_ids) > 1:
            c.execute('''
                SELECT councilor_id, name, election_year
                FROM councilors_councilorsdetail
                WHERE councilor_id in %s AND county = %s
            ''', [tuple(councilor_ids), person['county']])
            r = c.fetchall()
            uids = {x[0] for x in r}
            if len(uids) > 1:
                for i in r:
                    selected = ' selected' if i[0] == person['uid'] else ''
                    print ', '.join([x for x in i]) + selected
                raise Exception('If they are same person, need to check which should be delete!!\n')
        c.execute('''
            INSERT INTO councilors_councilorsdetail(councilor_id, election_year, name, gender, party, constituency, county, district, in_office, contact_details, education, experience, remark, image, links, platform)
            VALUES (%(uid)s, %(election_year)s, %(name)s, %(gender)s, %(party)s, %(constituency)s, %(county)s, %(district)s, %(in_office)s, %(contact_details)s, %(education)s, %(experience)s, %(remark)s, %(image)s, %(links)s, %(platform)s)
            ON CONFLICT (councilor_id, election_year)
            DO NOTHING
        ''', person)
conn.commit()

# update term_end councilors
term_end_councilors = json.load(open('../../data/term_end.json'))
c.executemany('''
    UPDATE councilors_councilorsdetail
    SET term_start = %(term_start)s
    WHERE county = %(county)s and election_year = %(election_year)s and name = %(name)s
''', term_end_councilors)

def rename_dict_key(d):
    columns = {
        u"去職原因": "reason",
        u"判決連結": "judicial_links",
        u"議員姓名": "name",
        u"選區": "constituency",
        u"政黨": "party",
        u"遞補議員": "replacement",
        u"遞補議員黨籍": "replacement_party",
        u"遞補議員性別": "replacement_gender",
        u"遞補議員生日": "replacement_birth",
        u"到職日": "term_start",
        u"去職日": "date",
        u"縣市": "county",
        u"遞補官方資訊": "ref"
    }
    for verbose_key, key in columns.items():
        d[key] = d.pop(verbose_key)
    return d

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credential.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_key('1ohhFgdHrxFZPcM7J-RqUskgZX2zqpYoxufNnX8VL4Os')
worksheets = sh.worksheets()
for wks in worksheets:
    rows = wks.get_all_records()
    for row in rows:
        row = rename_dict_key(row)
        row['election_year'] = wks.title
        if row['replacement']:
            replacement = {
                'county': row['county'],
                'constituency': row['constituency'],
                'election_year': row['election_year'],
                'name': row['replacement'],
                'party': row['replacement_party'],
                'gender': row['replacement_gender'],
                'birth': row['replacement_birth'],
                'in_office': True,
                'term_start': row['date']
            }
            replacement['uid'], created = common.get_or_create_councilor_uid(c, replacement)
            if not created:
                Councilors(replacement)
            c.execute('''
                INSERT INTO councilors_councilorsdetail(councilor_id, election_year, name, gender, party, constituency, county, in_office, term_start)
                VALUES (%(uid)s, %(election_year)s, %(name)s, %(gender)s, %(party)s, %(constituency)s, %(county)s, %(in_office)s, %(term_start)s)
                ON CONFLICT (councilor_id, election_year)
                DO UPDATE
                SET gender = %(gender)s, party = %(party)s, in_office = %(in_office)s, term_start = %(term_start)s
            ''', replacement)
            if replacement['birth']:
                c.execute('''
                    update councilors_councilors
                    SET birth = %(birth)s
                    where uid = %(uid)s
                ''', replacement)
        row['in_office'] = False
        row['uid'], created = common.get_or_create_councilor_uid(c, row)
        if not created:
            Councilors(row)
        row['term_end'] = {k: row.pop(k) for k in ['reason', 'judicial_links', 'replacement', 'date', 'ref']}
        c.execute('''
            INSERT INTO councilors_councilorsdetail(councilor_id, election_year, name, party, constituency, county, in_office, term_end)
            VALUES (%(uid)s, %(election_year)s, %(name)s, %(party)s, %(constituency)s, %(county)s, %(in_office)s, %(term_end)s)
            ON CONFLICT (councilor_id, election_year)
            DO UPDATE
            SET party = %(party)s, in_office = %(in_office)s, term_end = %(term_end)s
        ''', row)
        c.execute('''
            UPDATE councilors_councilorsdetail
            SET term_start = %(term_start)s
            WHERE councilor_id = %(uid)s AND election_year = %(election_year)s AND term_start is null
        ''', row)
conn.commit()
