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


def normalize_constituency(constituency):
    match = re.search(u'第(?P<num>.+)選(?:舉)?區', constituency)
    if not match:
        return ''
    ref = {u'一': 1, u'二': 2, u'三': 3, u'四': 4, u'五': 5, u'六': 6, u'七': 7, u'八': 8, u'九': 9, u'十': 10}
    digits = re.findall(u'(一|二|三|四|五|六|七|八|九|十)', match.group('num'))
    total, dec = 0, 1
    for i in reversed(range(0, len(digits))):
        total = total + int(ref.get(digits[i], 0)) * dec
        dec = dec * 10
    return total

def uid(councilor):
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
    c.execute('''
        SELECT councilor_id
        FROM councilors_councilorsdetail
        WHERE name = %(name)s and election_year = %(election_year)s and county = %(county)s
    ''', councilor)
    r = c.fetchone()
    if r:
        return r[0]

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
    complement['constituency'] = normalize_constituency(complement['constituency'])
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

for council in ['../../data/kcc/councilors_terms.json', '../../data/tcc/councilors_terms.json']:
    print council
    dict_list = json.load(open(council))
    for councilor in dict_list:
        councilor['uid'] = uid(councilor)
        Councilors(councilor)
        insertCouncilorsDetail(councilor)
    conn.commit()

for council in ['../../data/tcc/councilors.json']:
    print council
    dict_list = json.load(open(council))
    print len(dict_list)
    for councilor in dict_list:
        councilor['uid'] = select_uid(councilor)
        updateCouncilorsDetail(councilor)
    conn.commit()
