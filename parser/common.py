# -*- coding: utf-8 -*-
import re
import codecs
import psycopg2
import json
from datetime import datetime


def normalize_person_name(name):
    name = re.sub(u'[。˙・･•．.]', u'‧', name)
    name = re.sub(u'[　\s()（）’]', '',name)
    name = name.title()
    return name

def county_abbr2string(abbr):
    return {
        'ntp': u'新北市',
        'tcc': u'臺北市',
        'tycc': u'桃園市',
        'kmc': u'基隆市',
        'ilcc': u'宜蘭縣',
        'hcc': u'新竹縣',
        'hsinchucc': u'新竹市',
        'mcc': u'苗栗縣',
        'tccc': u'臺中市',
        'chcc': u'彰化縣',
        'ylcc': u'雲林縣',
        'ntcc': u'南投縣',
        'cyscc': u'嘉義縣',
        'cycc': u'嘉義市',
        'tncc': u'臺南市',
        'kcc': u'高雄市',
        'ptcc': u'屏東縣',
        'hlcc': u'花蓮縣',
        'taitungcc': u'臺東縣',
        'mtcc': u'連江縣',
        'kmcc': u'金門縣',
        'phcouncil': u'澎湖縣'
    }[abbr]

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

def getDetailIdFuzzy(c, name, election_year, county):
    m = re.match(u'(?P<cht>.+?)[a-zA-Z]', name)
    if m:
        name = m.group('cht')
    c.execute('''
        SELECT id
        FROM councilors_councilorsdetail
        WHERE name like %s and election_year = %s and county = %s
    ''', (name + '%', election_year, county))
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
    else:
        return getDetailIdFuzzy(c, name, election_year, county)

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
    #raw_input()
    return []

def GetCouncilorId(c, name):
    identifiers = {name, re.sub(u'[\w。˙・･•．.‧’]', '', name), re.sub(u'\W', '', name).lower(), } - {''}
    if identifiers:
        c.execute('''
            SELECT uid
            FROM councilors_councilors
            WHERE identifiers ?| array[%s]
        ''' % ','.join(["'%s'" % x for x in identifiers]))
        return [x[0] for x in c.fetchall()]

def getCouncilorIdList(c, text):
    id_list = []
    for name in text.split():
        name = re.sub(u'(.*)[）)。】」]$', '\g<1>', name) # 名字後有標點符號
        councilor_ids = GetCouncilorId(c, name)
        if councilor_ids:
            id_list.extend(councilor_ids)
        else:
            print u'%s not an councilor?' % name
    return id_list

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

def UpdateSittingLinks(c, meeting):
    c.execute('''
        UPDATE sittings_sittings
        SET links = %(links)s
        WHERE name = %(name)s
        RETURNING id
    ''', meeting)
    if not c.fetchall():
        c.execute('''
            UPDATE sittings_sittings
            SET links = %(links)s
            WHERE county = %(county)s AND date = %(date)s
        ''', meeting)
