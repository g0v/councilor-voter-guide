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


def uid(councilor):
    if councilor.get('birth'):
        c.execute('''
            SELECT uid
            FROM councilors_councilors
            WHERE name = %(name)s and birth = %(birth)s
        ''', councilor)
        r = c.fetchone()
        return r[0] if r else uuid.uuid4().hex
    c.execute('''
        SELECT councilor_id
        FROM councilors_councilorsdetail
        WHERE name = %(name)s and election_year != %(election_year)s and county = %(county)s
    ''', councilor)
    r = c.fetchone()
    if r:
        return r[0]
    c.execute('''
        SELECT councilor_id
        FROM councilors_councilorsdetail
        WHERE name = %(name)s and election_year != %(election_year)s
    ''', councilor)
    r = c.fetchone()
    return r[0] if r else uuid.uuid4().hex

def Councilors(councilor):
    councilor['former_names'] = '\n'.join(councilor['former_names']) if councilor.has_key('former_names') else ''
    complement = {"birth": None}
    complement.update(councilor)
    print complement
    c.execute('''
        INSERT INTO councilors_councilors(uid, name, birth, former_names)
        SELECT %(uid)s, %(name)s, %(birth)s, %(former_names)s
        WHERE NOT EXISTS (SELECT 1 FROM councilors_councilors WHERE uid = %(uid)s)
    ''', complement)

def CouncilorsDetail(councilor):
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
        complement = {"gender":'', "party":'', "contact_details":None, "title":'', "constituency":'', "county":'', "district":'', "in_office":True, "term_start":None, "term_end":{}, "education":None, "experience":None, "remark":None, "image":'', "links":None, "platform":''}
    complement.update(councilor)
    c.execute('''
        UPDATE councilors_councilorsdetail
        SET name = %(name)s, gender = %(gender)s, party = %(party)s, title = %(title)s, constituency = %(constituency)s, in_office = %(in_office)s, contact_details = %(contact_details)s, county = %(county)s, district = %(district)s, term_start = %(term_start)s, term_end = %(term_end)s, education = %(education)s, experience = %(experience)s, remark = %(remark)s, image = %(image)s, links = %(links)s, platform = %(platform)s
        WHERE councilor_id = %(uid)s and election_year = %(election_year)s
    ''', complement)
    c.execute('''
        INSERT into councilors_councilorsdetail(councilor_id, election_year, name, gender, party, title, constituency, county, district, in_office, contact_details, term_start, term_end, education, experience, remark, image, links, platform)
        SELECT %(uid)s, %(election_year)s, %(name)s, %(gender)s, %(party)s, %(title)s, %(constituency)s, %(county)s, %(district)s, %(in_office)s, %(contact_details)s, %(term_start)s, %(term_end)s, %(education)s, %(experience)s, %(remark)s, %(image)s, %(links)s, %(platform)s
        WHERE NOT EXISTS (SELECT 1 FROM councilors_councilorsdetail WHERE councilor_id = %(uid)s and election_year = %(election_year)s ) RETURNING id
    ''', complement)

conn = db_settings.con()
c = conn.cursor()

for council in ['../../data/kcc/councilors_terms.json', '../../data/tcc/councilors_terms.json', '../../data/tcc/councilors.json']:
    print council
    dict_list = json.load(open(council))
    for councilor in dict_list:
        councilor['uid'] = uid(councilor)
        Councilors(councilor)
        CouncilorsDetail(councilor)
    conn.commit()
