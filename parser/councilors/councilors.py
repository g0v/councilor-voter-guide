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
    councilor['name'] = re.sub(u'[。˙・･•．.]', u'‧', councilor['name'])
    councilor['name'] = re.sub(u'[　\s]', '', councilor['name'])
    councilor['name'] = re.sub(u'(副?議長|議員)', '', councilor['name'])
    councilor['gender'] = re.sub(u'性', '', councilor.get('gender', ''))
    if councilor.get('party'):
        councilor['party'] = councilor['party'].strip()
        councilor['party'] = re.sub(u'籍$', '', councilor['party'])
        councilor['party'] = re.sub(u'無黨?$', u'無黨籍', councilor['party'])
        councilor['party'] = re.sub(u'台灣', u'臺灣', councilor['party'])
        councilor['party'] = re.sub(u'台聯黨', u'臺灣團結聯盟', councilor['party'])
        councilor['party'] = re.sub(u'^國民黨$', u'中國國民黨', councilor['party'])
        councilor['party'] = re.sub(u'^民進黨$', u'民主進步黨', councilor['party'])
    councilor['constituency'] = get_constituency(councilor)
    councilor['constituency'] = normalize_constituency(councilor['constituency'])
    return councilor

def get_or_create_uid(councilor):
    logging.info(councilor)
    print councilor['name']
    councilor['councilor_ids'] = tuple(common.GetCouncilorId(c, councilor['name']))
    c.execute('''
        SELECT councilor_id
        FROM councilors_councilorsdetail
        WHERE councilor_id in %(councilor_ids)s
        ORDER BY
            CASE
                WHEN election_year = %(election_year)s AND county = %(county)s AND constituency = %(constituency)s AND name = %(name)s THEN 1
                WHEN election_year = %(election_year)s AND county = %(county)s AND constituency = %(constituency)s THEN 2
                WHEN county = %(county)s AND constituency = %(constituency)s AND name = %(name)s THEN 3
                WHEN county = %(county)s AND constituency = %(constituency)s THEN 4
                WHEN county = %(county)s AND name = %(name)s THEN 5
                WHEN county = %(county)s THEN 6
            END,
            election_year DESC
        LIMIT 1
    ''', councilor)
    r = c.fetchone()
    return r[0] if r else uuid.uuid4().hex

def Councilors(councilor):
    councilor['former_names'] = councilor.get('former_names', [])
    variants = set()
    for variant in [(u'温', u'溫'), (u'黄', u'黃'), (u'寳', u'寶'), (u'真', u'眞'), (u'福', u'褔'), (u'鎭', u'鎮'), (u'姸', u'妍'), (u'市', u'巿'), (u'衛', u'衞'), (u'館', u'舘'), (u'峰', u'峯'), (u'群', u'羣'), (u'啓', u'啟'), (u'鳳', u'鳯'), (u'冗', u'宂'), ]:
        variants.add(re.sub(variant[0], variant[1], councilor['name']))
        variants.add(re.sub(variant[1], variant[0], councilor['name']))
    councilor['identifiers'] = list((variants | set(councilor['former_names']) | {councilor['name'], re.sub(u'[\w‧’]]', '', councilor['name']), re.sub(u'\W', '', councilor['name']).lower(), }) - {''})
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
    WHERE identifiers is null
''')
key = [desc[0] for desc in c.description]
for row in c.fetchall():
    person = dict(zip(key, row))
    person['name'] = person['name'].decode('utf-8')
    Councilors(person)
conn.commit()

# upsert from json
for council in ['../../data/phcouncil/councilors.json', '../../data/kmcc/councilors.json', '../../data/mtcc/councilors.json', '../../data/ptcc/councilors.json', '../../data/kcc/councilors.json', '../../data/tncc/councilors.json', '../../data/taitungcc/councilors.json', '../../data/hlcc/councilors.json', '../../data/cycc/councilors.json', '../../data/cyscc/councilors.json', '../../data/ylcc/councilors.json', '../../data/ntcc/councilors.json', '../../data/chcc/councilors.json', '../../data/tccc/councilors.json', '../../data/ilcc/councilors.json', '../../data/mcc/councilors.json', '../../data/hcc/councilors.json', '../../data/kmc/councilors.json', '../../data/tycc/councilors.json', '../../data/hsinchucc/councilors.json', '../../data/ntp/councilors.json', '../../data/tcc/councilors.json']:
    print council
    dict_list = json.load(open(council))
    for councilor in dict_list:
        councilor = normalize_councilor(councilor)
        councilor['uid'] = get_or_create_uid(councilor)
        Councilors(councilor)
        insertCouncilorsDetail(councilor)
        if councilor['in_office']:
            examinate_with_cand_moi(councilor)
conn.commit()

# update term_end councilors
term_end_councilors = json.load(open('../../data/term_end.json'))
c.executemany('''
    UPDATE councilors_councilorsdetail
    SET term_start = %(term_start)s
    WHERE county = %(county)s and election_year = %(election_year)s and name = %(name)s
''', term_end_councilors)
conn.commit()
