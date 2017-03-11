#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import json
import uuid
import codecs
import psycopg2
from psycopg2.extras import Json
import db_settings
import common


def get_constituency(councilor):
    if councilor.get('constituency'):
        return councilor['constituency']
    try:
        for k, v in constituency_maps[councilor['county']][councilor['election_year']].iteritems():
            if v == councilor['district']:
                return k
    except:
        return ''
    return ''

def normalize_constituency(constituency):
    match = re.search(u'第(?P<num>.+)選(?:舉)?區', constituency)
    if not match:
        return ''
    try:
        return int(match.group('num'))
    except:
        print match.group('num')
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
    # same name and county different election_year first
    c.execute('''
        SELECT councilor_id
        FROM councilors_councilorsdetail
        WHERE name = %(name)s and election_year != %(election_year)s and county = %(county)s
    ''', councilor)
    r = c.fetchone()
    if r:
        return r[0]
    # same name different election_year
    c.execute('''
        SELECT councilor_id
        FROM councilors_councilorsdetail
        WHERE name = %(name)s and election_year != %(election_year)s
    ''', councilor)
    r = c.fetchone()
    return r[0] if r else uuid.uuid4().hex

def select_uid(councilor):
    print councilor
    c.execute('''
        SELECT councilor_id
        FROM councilors_councilorsdetail
        WHERE name = %(name)s and election_year = %(election_year)s and county = %(county)s
    ''', councilor)
    r = c.fetchone()
    if r:
        return r[0]
    else:
        return get_or_create_uid(councilor)

def Councilors(councilor):
    councilor['former_names'] = '\n'.join(councilor['former_names']) if councilor.has_key('former_names') else ''
    complement = {"birth": None}
    complement.update(councilor)
    c.execute('''
        INSERT INTO councilors_councilors(uid, name, birth, former_names)
        SELECT %(uid)s, %(name)s, %(birth)s, %(former_names)s
        WHERE NOT EXISTS (SELECT 1 FROM councilors_councilors WHERE uid = %(uid)s)
    ''', complement)

def updateCouncilorsDetail(councilor):
    for key in ['education', 'experience', 'platform', 'remark']:
        if councilor.has_key(key):
            councilor[key] = '\n'.join(councilor[key])
    c.execute('''
        SELECT *
        FROM councilors_councilorsdetail
        WHERE councilor_id = %(uid)s and election_year = %(election_year)s
    ''', councilor)
    key = [desc[0] for desc in c.description]
    r = c.fetchone()
    if r:
        complement = dict(zip(key, r))
    else:
        print councilor
        raw_input()
    complement.update(councilor)
    c.execute('''
        UPDATE councilors_councilorsdetail
        SET name = %(name)s, gender = %(gender)s, party = %(party)s, title = %(title)s, constituency = %(constituency)s, in_office = %(in_office)s, contact_details = %(contact_details)s, county = %(county)s, district = %(district)s, term_start = %(term_start)s, term_end = %(term_end)s, education = %(education)s, experience = %(experience)s, remark = %(remark)s, image = %(image)s, links = %(links)s, platform = %(platform)s
        WHERE councilor_id = %(uid)s and election_year = %(election_year)s
    ''', complement)

def insertCouncilorsDetail(councilor):
    for key in ['education', 'experience', 'platform', 'remark']:
        if councilor.has_key(key):
            councilor[key] = '\n'.join(councilor[key])
    complement = {"gender":'', "party":'', "contact_details":None, "title":'', "constituency":'', "county":'', "district":'', "in_office":True, "term_start":None, "term_end":{}, "education":None, "experience":None, "remark":None, "image":'', "links":None, "platform":''}
    complement.update(councilor)
    c.execute('''
        INSERT into councilors_councilorsdetail(councilor_id, election_year, name, gender, party, title, constituency, county, district, in_office, contact_details, term_start, term_end, education, experience, remark, image, links, platform)
        SELECT %(uid)s, %(election_year)s, %(name)s, %(gender)s, %(party)s, %(title)s, %(constituency)s, %(county)s, %(district)s, %(in_office)s, %(contact_details)s, %(term_start)s, %(term_end)s, %(education)s, %(experience)s, %(remark)s, %(image)s, %(links)s, %(platform)s
        WHERE NOT EXISTS (SELECT 1 FROM councilors_councilorsdetail WHERE councilor_id = %(uid)s and election_year = %(election_year)s ) RETURNING id
    ''', complement)

conn = db_settings.con()
c = conn.cursor()
constituency_maps = json.load(open('../constituency.json'))
# insert
for council in ['../../data/tccc/councilors.json', '../../data/ilcc/councilors.json', '../../data/mcc/councilors.json', '../../data/hcc/councilors.json', '../../data/kmc/councilors.json', '../../data/tycc/councilors.json', '../../data/hsinchucc/councilors.json', '../../data/ntp/councilors_terms.json', '../../data/ntp/councilors.json', '../../data/tcc/councilors.json']:
    print council
    dict_list = json.load(open(council))
    for councilor in dict_list:
        councilor = normalize_councilor(councilor)
        councilor['uid'] = select_uid(councilor)
        Councilors(councilor)
        insertCouncilorsDetail(councilor)
conn.commit()

## update
#for council in ['../../data/mcc/councilors.json', ]:
#    print council
#    dict_list = json.load(open(council))
#    for councilor in dict_list:
#        councilor = normalize_councilor(councilor)
#        councilor['uid'] = select_uid(councilor)
#        updateCouncilorsDetail(councilor)
#conn.commit()

# update term_end councilors
term_end_councilors = json.load(open('../../data/term_end.json'))
c.executemany('''
    UPDATE councilors_councilorsdetail
    SET term_start = %(term_start)s
    WHERE county = %(county)s and election_year = %(election_year)s and name = %(name)s
''', term_end_councilors)
conn.commit()
