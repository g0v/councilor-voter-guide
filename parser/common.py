# -*- coding: utf-8 -*-
import re
import codecs
import psycopg2
import json
from datetime import datetime


def SittingsAbbreviation(key):
    d = json.load(open('util.json'))
    return d.get(key)

def FileLog(c, sitting):
    c.execute('''
        INSERT into councilors_filelog(sitting, date)
        SELECT %s, %s
        WHERE NOT EXISTS (SELECT 1 FROM councilors_filelog WHERE sitting = %s) RETURNING id
    ''', (sitting, datetime.now(), sitting))

def ROC2AD(text):
    matchTerm = re.search(u'''
        (?P<year>[\d]+)[\s]*(?:年|[-/.])[\s]*
        (?P<month>[\d]+)[\s]*(?:月|[-/.])[\s]*
        (?P<day>[\d]+)
    ''', text, re.X)
    if matchTerm:
        return '%04d-%02d-%02d' % (int(matchTerm.group('year'))+1911, int(matchTerm.group('month')), int(matchTerm.group('day')))

def getId(c, name, election_year, county):
    c.execute('''
        SELECT councilor_id
        FROM councilors_councilorsdetail
        WHERE name = %s and election_year = %s and county = %s
    ''', (name, election_year, county))
    r = c.fetchone()
    if r:
        return r[0]
    print '"%s"' % name

def getDetailId(c, name, election_year, county):
    c.execute('''
        SELECT id
        FROM councilors_councilorsdetail
        WHERE name = %s and election_year = %s and county = %s
    ''', (name, election_year, county))
    r = c.fetchone()
    if r:
        return r[0]
    print '"%s"' % name

def getIdList(c, name_list, sitting_dict):
    c.execute('''
        SELECT id, councilor_id
        FROM councilors_councilorsdetail
        WHERE name IN %s and election_year = %s and county = %s
    ''', (tuple(name_list), sitting_dict['election_year'], sitting_dict['county']))
    r = c.fetchall()
    if r:
        return r
    for name in name_list:
        print '"%s"' % name
    raw_input()
    return []

def getNameList(text):
    name_list, firstName = [], ''
    for name in text.split():
        if re.search(u'[）)。】」]$', name):   #名字後有標點符號
            name = name[:-1]
        #中文姓名中間有空白
        if len(name) < 2 and firstName == '':
            firstName = name
            continue
        if firstName != '':
            name = firstName + name
            firstName = ''
        name_list.append(name)
    return name_list

def AddAttendanceRecord(c, councilor_id, sitting_id, category, status):
    c.execute('''
        INSERT into councilors_attendance(councilor_id, sitting_id, category, status)
        SELECT %s, %s, %s, %s
        WHERE NOT EXISTS (SELECT 1 FROM councilors_attendance WHERE councilor_id = %s AND sitting_id = %s)
    ''', (councilor_id, sitting_id, category, status, councilor_id, sitting_id))

def Attendance(c, sitting_dict, text, category, status):
    ids = []
    for id, councilor_id in getIdList(c, getNameList(text), sitting_dict):
        AddAttendanceRecord(c, id, sitting_dict['uid'], category, status)
        ids.append(id)
    return ids

def InsertSitting(c, sitting_dict):
    complement = {"committee": '', "name": ''}
    complement.update(sitting_dict)
    c.execute('''
        UPDATE sittings_sittings
        SET name = %(name)s, election_year = %(election_year)s, date = %(date)s, county = %(county)s, committee = %(committee)s
        WHERE uid = %(uid)s
    ''', complement)
    c.execute('''
        INSERT into sittings_sittings(uid, name, election_year, date, county, committee)
        SELECT %(uid)s, %(name)s, %(election_year)s, %(date)s, %(county)s, %(committee)s
        WHERE NOT EXISTS (SELECT 1 FROM sittings_sittings WHERE uid = %(uid)s)
    ''', complement)

def UpdateSitting(c, uid, name):
    c.execute('''
        UPDATE sittings_sittings
        SET name = %s
        WHERE uid = %s
    ''', (name, uid))

def remote_newline_in_sittings(c):
    c.execute('''
        select uid, name
        from sittings_sittings
    ''')
    for uid, name in c.fetchall():
        UpdateSitting(c, uid, re.sub(u'[\s]', '', name))
