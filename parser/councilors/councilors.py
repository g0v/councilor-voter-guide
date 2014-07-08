#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import json
import codecs
import psycopg2
from psycopg2.extras import Json
import db_settings
import common


def Councilors(councilor):
    if councilor.has_key('former_names'):
        councilor['former_names'] = '\n'.join(councilor['former_names'])
    else:
        councilor.update({'former_names': ''})
    c.execute('''
        UPDATE councilors_councilors
        SET name = %(name)s, birth = %(birth)s, former_names = %(former_names)s
        WHERE uid = %(uid)s
    ''', councilor)
    c.execute('''
        INSERT INTO councilors_councilors(uid, name, birth, former_names)
        SELECT %(uid)s, %(name)s, %(birth)s, %(former_names)s
        WHERE NOT EXISTS (SELECT 1 FROM councilors_councilors WHERE uid = %(uid)s)
    ''', councilor)

def CouncilorsDetail(councilor, ideal_term_end_year):
    if councilor.has_key('education'):
        councilor['education'] = '\n'.join(councilor['education'])
    if councilor.has_key('experience'):
        councilor['experience'] = '\n'.join(councilor['experience'])
    if councilor.has_key('platform'):
        councilor['platform'] = '\n'.join(councilor['platform'])
    if councilor.has_key('remark'):
        councilor['remark'] = '\n'.join(councilor['remark'])
    c.execute('''
        SELECT *
        FROM councilors_councilorsdetail
        WHERE councilor_id = %(uid)s and ad = %(ad)s
    ''', councilor)
    key = [desc[0] for desc in c.description]
    r = c.fetchone()
    if r:
        complement = dict(zip(key, r))
    else:
        complement = {"gender":'', "party":'', "contacts":None, "title":'', "constituency":'', "county":'', "district":'', "term_start":'%04d-12-25' % int(ideal_term_end_year[councilor['ad']-1]), "term_end":{"date": '%04d-12-25' % int(ideal_term_end_year[councilor['ad']])}, "education":None, "experience":None, "remark":None, "image":'', "links":None, "platform":''}
    complement.update(councilor)
    c.execute('''
        UPDATE councilors_councilorsdetail
        SET name = %(name)s, gender = %(gender)s, party = %(party)s, title = %(title)s, constituency = %(constituency)s, in_office = %(in_office)s, contacts = %(contacts)s, county = %(county)s, district = %(district)s, term_start = %(term_start)s, term_end = %(term_end)s, education = %(education)s, experience = %(experience)s, remark = %(remark)s, image = %(image)s, links = %(links)s, platform = %(platform)s
        WHERE councilor_id = %(uid)s and ad = %(ad)s
    ''', complement)
    c.execute('''
        INSERT into councilors_councilorsdetail(councilor_id, ad, name, gender, party, title, constituency, county, district, in_office, contacts, term_start, term_end, education, experience, remark, image, links, platform)
        SELECT %(uid)s, %(ad)s, %(name)s, %(gender)s, %(party)s, %(title)s, %(constituency)s, %(county)s, %(district)s, %(in_office)s, %(contacts)s, %(term_start)s, %(term_end)s, %(education)s, %(experience)s, %(remark)s, %(image)s, %(links)s, %(platform)s
        WHERE NOT EXISTS (SELECT 1 FROM councilors_councilorsdetail WHERE councilor_id = %(uid)s and ad = %(ad)s ) RETURNING id
    ''', complement)

conn = db_settings.con()
c = conn.cursor()

for council in ['../../data/taipei/councilor_1-11.json', '../../data/taipei/councilor-11.json', '../../data/tncc/tnccp.json']:
    dict_list = json.load(open(council))
    ideal_term_end_year = {0:1969, 1:1973, 2:1977, 3:1981, 4:1985, 5:1989, 6:1994, 7:1998, 8:2002, 9:2006, 10:2010, 11:2014}
    for councilor in dict_list:
        councilor.update({'uid': '%s_%s' % (councilor['name'], councilor['birth']), 'in_office': True})
        councilor['ad'] = int(councilor['ad'])
        Councilors(councilor)
        CouncilorsDetail(councilor, ideal_term_end_year)
    conn.commit()
