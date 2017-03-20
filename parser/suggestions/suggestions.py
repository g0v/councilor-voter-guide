#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import glob
import json
import codecs
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

def get_election_year(county, suggest_year):
    c.execute('''
        SELECT election_year
        FROM councilors_councilorsdetail
        WHERE county = %s
        GROUP BY election_year
        ORDER BY election_year desc
    ''', (county,))
    r = c.fetchall()
    for election_year in r:
        if int(suggest_year) > int(election_year[0]):
            return election_year[0]

def getCouncilordetailIdList(id_list, election_year, county):
    if id_list:
        c.execute('''
            SELECT id
            FROM councilors_councilorsdetail
            WHERE councilor_id IN %s and election_year = %s and county = %s
        ''', (tuple(id_list), election_year, county))
        r = c.fetchall()
        if r:
            return r[0]
        for id in id_list:
            print election_year, county, id
            raw_input()

def normalize_person_name(name):
    name = re.sub(u'[。˙・･•．.]', u'‧', name)
    name = re.sub(u'[　()（）]', '', name)
    name = re.sub(u'(副?議長|議員)', '', name)
    name = re.sub(u'、', ' ', name)
    for wrong, right in [(u'游輝', u'游輝宂'), (u'連婓璠', u'連斐璠'), (u'羅文幟', u'羅文熾'), (u'郭昭嚴', u'郭昭巖'), (u'闕梅莎', u'闕枚莎'), (u'林亦華', u'林奕華'), (u'周鍾$', u'周鍾㴴'), (u'汪志銘', u'汪志冰'), (u'簡余宴', u'簡余晏'), (u'周佑威', u'周威佑'), (u'黃洋', u'黃平洋'), (u'周玲玟', u'周玲妏')]:
        name = re.sub(wrong, right, name)
    name = name.title()
    return name

conn = db_settings.con()
c = conn.cursor()
df_concat = DataFrame()
for meta_file in glob.glob('../../data/*/suggestions.json'):
    county_abbr = meta_file.split('/')[-2]
    county = common.county_abbr2string(county_abbr)
    with open(meta_file) as meta_file:
        metas = json.load(meta_file)
        for meta in metas:
            if meta['file_ext'] == 'ods':
                continue
            meta['county'] = county
            file_name = '{year}_{month_from}-{month_to}.{file_ext}'.format(**meta)
            print file_name
            f = '../../data/%s/suggestions/%s' % (county_abbr, file_name)
            df = pd.read_excel(f, sheetname=0, header=None, encoding='utf-8')
            if len(df.columns) < 9 or not re.search(u'姓名', df.iloc[3:5, 0].to_string(na_rep='', index=False)):
                print 'no name column!!'
                continue
            df = pd.read_excel(f, sheetname=0, header=None, usecols=range(0, 9), skiprows=5, names=['councilor', 'suggestion', 'position', 'suggest_expense', 'approved_expense', 'expend_on', 'brought_by', 'bid_type', 'bid_by'], encoding='utf-8')
            for key in ['councilor', 'position', 'suggest_expense', 'brought_by', ]:
                df[key].fillna(inplace=True, method='pad')
            election_year = get_election_year(county, meta['year'])
            df['election_year'] = election_year
            df['county'] = county
            df['suggest_year'] = meta['year']
            df['suggest_month'] = meta['month_to']
            df['uid'] = map(lambda x: u'{county}-{year}-{month_from}-{month_to}'.format(**meta) + '-%d' % (x+6), df.index)
            df.dropna(inplace=True, how='any', subset=['suggestion'])
            df['councilor'] = map(lambda x: normalize_person_name(x) if x else nan, df['councilor'])
            df['councilor_ids'] = map(lambda x: getCouncilordetailIdList(common.getCouncilorIdList(c, x), election_year, county) if x else nan, df['councilor'])
            df['suggest_expense'] = map(lambda x: x*1000 if is_number(x) else nan, df['suggest_expense'])
            df['approved_expense'] = map(lambda x: x*1000 if is_number(x) else nan, df['approved_expense'])
            df_concat = concat([df_concat, df])
print 'df: ', df_concat

def Suggestions(suggestion):
    for column in ['position', 'expend_on', 'brought_by', 'bid_type', 'bid_by']:
        suggestion[column] = suggestion[column].strip() if suggestion[column] else ''
    suggestion['bid_by'] = suggestion['bid_by'].split()
    if len(suggestion['bid_by']) == 1:
        suggestion['bid_by'] = suggestion['bid_by'][0].split(u'、')
    c.execute('''
        INSERT INTO suggestions_suggestions(uid, county, election_year, suggest_year, suggest_month, suggestion, position, suggest_expense, approved_expense, expend_on, brought_by, bid_type, bid_by, district, constituency)
        VALUES (%(uid)s, %(county)s, %(election_year)s, %(suggest_year)s, %(suggest_month)s, %(suggestion)s, %(position)s, %(suggest_expense)s, %(approved_expense)s, %(expend_on)s, %(brought_by)s, %(bid_type)s, %(bid_by)s, %(district)s, %(constituency)s)
        ON CONFLICT (uid)
        DO UPDATE
        SET county = %(county)s, election_year = %(election_year)s, suggest_year = %(suggest_year)s, suggest_month = %(suggest_month)s, suggestion = %(suggestion)s, position = %(position)s, suggest_expense = %(suggest_expense)s, approved_expense = %(approved_expense)s, expend_on = %(expend_on)s, brought_by = %(brought_by)s, bid_type = %(bid_type)s, bid_by = %(bid_by)s, district = %(district)s, constituency = %(constituency)s
    ''', suggestion)

def CouncilorsSuggestions(suggestion):
    c.execute('''
        INSERT INTO suggestions_councilors_suggestions(councilor_id, suggestion_id, jurisdiction)
        VALUES (%(councilor_id)s, %(uid)s, %(jurisdiction)s)
        ON CONFLICT (councilor_id, suggestion_id)
        DO UPDATE
        SET jurisdiction = %(jurisdiction)s
    ''', suggestion)

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

#files = [f for f in glob.glob('../../data/*/suggestions/*.json')]
#for f in files:
#    print open(f).name
#    df = pd.read_json(f, orient='records', dtype=False)
#    df_concat = concat([df_concat, df])
#df_concat.to_json('../../data/suggestions.json', orient='records', force_ascii=False)
ds = df_concat.to_json(orient='records', force_ascii=False)
dict_list = json.loads(ds)
print len(dict_list)
for item in dict_list:
    if not item['councilor_ids']:
        continue
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
