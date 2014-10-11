#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import glob
import json
import psycopg2
from psycopg2.extras import Json
from pandas import *
import pandas as pd
from numpy import nan
import common
import db_settings


def is_number(text):
    try:
        float(text)
        return True
    except:
        return False

def getIdList(name_list, election_year, county):
    c.execute('''
        SELECT id
        FROM councilors_councilorsdetail
        WHERE name IN %s and election_year = %s and county = %s
    ''', (tuple(name_list), election_year, county))
    r = c.fetchall()
    if r:
        return r[0]
    for name in name_list:
        print '"%s"' % name

conn = db_settings.con()
c = conn.cursor()
files = [f for f in glob.glob('../../data/*/suggestions/*')]
df_concat = DataFrame()
for f in files:
    print open(f, 'r').name
    df = pd.read_excel(f, sheetname=0, header=None, encoding='utf-8')
    county = re.search(u'\S*?[縣市]', df.icol(0)[0]).group()
    year, month = re.sub('\D', ' ', df.icol(0)[1]).split()
    if year != '103' and month != '12':
        continue
    df = pd.read_excel(f, sheetname=0, header=None, usecols=range(0, 9), skiprows=5, names=['councilor', 'suggestion', 'position', 'suggest_expense', 'approved_expense', 'expend_on', 'brought_by', 'bid_type', 'bid_by'], encoding='utf-8')
    df.dropna(inplace=True, how='any', subset=['suggestion'])
    df['councilor'] = map(lambda x: re.sub(u'[\s　]$', '', x) if x else nan, df['councilor'])
    df['councilor'] = map(lambda x: re.sub(u'[.．]', u'‧', x) if x else nan, df['councilor'])
    df['councilor'] = map(lambda x: re.sub(u'、', ' ', x) if x else nan, df['councilor'])
    for wrong, right in [(u'郭昭嚴', u'郭昭巖'), (u'闕梅莎', u'闕枚莎'), (u'林亦華', u'林奕華'), (u'周鍾$', u'周鍾㴴'), (u'汪志銘', u'汪志冰'), (u'簡余宴', u'簡余晏'), (u'周佑威', u'周威佑'), (u'黃洋', u'黃平洋'), (u'周玲玟', u'周玲妏')]:
        df['councilor'] = map(lambda x: re.sub(wrong, right, x) if x else nan, df['councilor'])
    df['councilor_ids'] = map(lambda x: getIdList(common.getNameList(x), '2010', county) if x else nan, df['councilor'])
    df['suggest_expense'] = map(lambda x: x*1000 if is_number(x) else nan, df['suggest_expense'])
    df['approved_expense'] = map(lambda x: x*1000 if is_number(x) else nan, df['approved_expense'])
    df['county'] = county
    df['suggest_year'] = str(int(year) + 1911)
    df['suggest_month'] = month
    df['uid'] = map(lambda x: '%s-%d-%d' % (county, int(year)+1911, x+6), df.index)
    df_concat = concat([df_concat, df])

def Suggestions(suggestion):
    for column in ['position', 'expend_on', 'brought_by', 'bid_type', 'bid_by']:
        suggestion[column] = suggestion[column].strip() if suggestion[column] else ''
    c.execute('''
        UPDATE suggestions_suggestions
        SET county = %(county)s, election_year = %(election_year)s, suggest_year = %(suggest_year)s, suggest_month = %(suggest_month)s, suggestion = %(suggestion)s, position = %(position)s, suggest_expense = %(suggest_expense)s, approved_expense = %(approved_expense)s, expend_on = %(expend_on)s, brought_by = %(brought_by)s, bid_type = %(bid_type)s, bid_by = %(bid_by)s, district = %(district)s, constituency = %(constituency)s
        WHERE uid = %(uid)s
    ''', suggestion)
    c.execute('''
        INSERT into suggestions_suggestions(uid, county, election_year, suggest_year, suggest_month, suggestion, position, suggest_expense, approved_expense, expend_on, brought_by, bid_type, bid_by, district, constituency)
        SELECT %(uid)s, %(county)s, %(election_year)s, %(suggest_year)s, %(suggest_month)s, %(suggestion)s, %(position)s, %(suggest_expense)s, %(approved_expense)s, %(expend_on)s, %(brought_by)s, %(bid_type)s, %(bid_by)s, %(district)s, %(constituency)s
        WHERE NOT EXISTS (SELECT 1 FROM suggestions_suggestions WHERE uid = %(uid)s)
    ''', suggestion)

def CouncilorsSuggestions(suggestion):
    c.execute('''
        UPDATE suggestions_councilors_suggestions
        SET jurisdiction = %(jurisdiction)s
        WHERE councilor_id = %(councilor_id)s AND suggestion_id = %(uid)s
    ''', suggestion)
    c.execute('''
        INSERT into suggestions_councilors_suggestions(councilor_id, suggestion_id, jurisdiction)
        SELECT %(councilor_id)s, %(uid)s, %(jurisdiction)s
        WHERE NOT EXISTS (SELECT 1 FROM suggestions_councilors_suggestions WHERE councilor_id = %(councilor_id)s AND suggestion_id = %(uid)s)
    ''', suggestion)

def get_election_year(suggestion):
    c.execute('''
        SELECT election_year
        FROM councilors_councilorsdetail
        WHERE county = %(county)s
        GROUP BY election_year
        ORDER BY election_year desc
    ''', suggestion)
    r = c.fetchall()
    for election_year in r:
        if int(suggestion['suggest_year']) >= int(election_year[0]):
            return election_year

def get_district(text, suggestion):
    if not text:
        return None, None
    for councilor_id in item['councilor_ids']:
        c.execute('''
            SELECT constituency, district
            FROM councilors_councilorsdetail
            WHERE id = %s AND district != ''
        ''', (councilor_id, ))
        r = c.fetchall()
        for constituency, district in r:
            for region in district.decode('utf-8').split(u'、'):
                if text.find(region) != -1:
                    return int(constituency), region
    c.execute('''
        SELECT constituency, district
        FROM councilors_councilorsdetail
        WHERE county = %(county)s AND election_year = %(election_year)s AND district != ''
        GROUP BY constituency, district
        ORDER BY constituency, district
    ''', suggestion)
    r = c.fetchall()
    for constituency, district in r:
        for region in district.decode('utf-8').split(u'、'):
            if text.find(region) != -1:
                return int(constituency), region
    return None, None

def get_jurisdiction(suggestion):
    c.execute('''
        SELECT *
        FROM councilors_councilorsdetail
        WHERE id = %(councilor_id)s AND constituency = %(constituency)s
    ''', suggestion)
    r = c.fetchall()
    return True if r else False

df_concat.to_json('../../data/suggestions.json', orient='records', force_ascii=False)
ds = df_concat.to_json(orient='records', force_ascii=False)
dict_list = json.loads(ds)
print len(dict_list)
for item in dict_list:
    if not item['councilor_ids']:
        print item
        raw_input()
        continue
    item['election_year'] = get_election_year(item)
    for column in ['position', 'suggestion', 'brought_by']:
        item['constituency'], item['district'] = get_district(item[column], item)
        if item['constituency']:
            break
    Suggestions(item)
    for councilor_id in item['councilor_ids']:
        item['councilor_id'] = councilor_id
        item['constituency'] = str(item['constituency'])
        item['jurisdiction'] = get_jurisdiction(item) if item['constituency'] else None
        CouncilorsSuggestions(item)
conn.commit()
