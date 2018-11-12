#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import glob
import json
import codecs
import subprocess
from pandas import *
import pandas as pd
from numpy import nan
import logging
import ast
from sys import argv

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
            return [x[0] for x in r]
        for id in id_list:
            logging.error("Can't find this counculor at this year : %s, %s, %s" % (election_year, county, id))
#           raw_input()

def normalize_person_name(name):
    name = re.sub(u'(副?議長|議員)[.]', '\n', name)
    name = re.sub(u'[。˙・･•．.]', u'‧', name)
    name = re.sub(u' {3}', '\n', name)
    name = re.sub(u'[　()（） ]', '', name)
    name = re.sub(u'(副?議長|議員)', '', name)
    name = re.sub(u'[、/;]', '\n', name)
    if len(name) > 5:
        name = re.sub(u'(\W+)和(\W+)', u'\g<1>\n\g<2>', name)
#   for wrong, right in [(u'游輝', u'游輝宂'), (u'連婓璠', u'連斐璠'), (u'羅文幟', u'羅文熾'), (u'郭昭嚴', u'郭昭巖'), (u'闕梅莎', u'闕枚莎'), (u'林亦華', u'林奕華'), (u'周鍾$', u'周鍾㴴'), (u'汪志銘', u'汪志冰'), (u'簡余宴', u'簡余晏'), (u'周佑威', u'周威佑'), (u'黃洋', u'黃平洋'), (u'周玲玟', u'周玲妏')]:
#       name = re.sub(wrong, right, name)
    name = name.title()
    return name

def sheet2df(target_sheet=0):
    df = pd.read_excel(f, sheetname=target_sheet, header=None, encoding='utf-8')
    no_person_name = False
    if not re.search(u'(姓名|名稱)', df.iloc[3:5, 0].to_string(na_rep='', index=False)):
        header_label = df.iloc[3:5, 8].to_string(na_rep='', index=False).strip()
        if len(df.columns) > 8 and (header_label == '' or header_label == u'單位'):
            should_drop_column = 8
        else:
            should_drop_column = 0
        no_person_name = True
    election_year = get_election_year(county, meta['year'])
    if len(df.columns) < 9:
        logging.info('no name column!!')
        df = pd.read_excel(f, sheetname=target_sheet, header=None, usecols=range(0, 8), skiprows=5, names=['suggestion', 'position', 'suggest_expense', 'approved_expense', 'expend_on', 'brought_by', 'bid_type', 'bid_by'], encoding='utf-8')
        df.dropna(inplace=True, how='any', subset=['suggestion', 'position', 'approved_expense'])
        for key in ['position', 'suggest_expense', 'brought_by', ]:
            df[key].fillna(inplace=True, method='pad')
        df['councilor_num'] = 1
        df['suggestor_name'] = nan
    else:
        if no_person_name:
            if should_drop_column == 0:
                df = pd.read_excel(f, sheetname=target_sheet, header=None, usecols=range(1, 9), skiprows=5, names=['suggestion', 'position', 'suggest_expense', 'approved_expense', 'expend_on', 'brought_by', 'bid_type', 'bid_by'], encoding='utf-8')
            elif should_drop_column == 8:
                df = pd.read_excel(f, sheetname=target_sheet, header=None, usecols=range(0, 8), skiprows=5, names=['suggestion', 'position', 'suggest_expense', 'approved_expense', 'expend_on', 'brought_by', 'bid_type', 'bid_by'], encoding='utf-8')
            df.dropna(inplace=True, how='any', subset=['suggestion', 'position', 'approved_expense'])
            for key in ['position', 'suggest_expense', 'brought_by', ]:
                df[key].fillna(inplace=True, method='pad')
            df['councilor_num'] = 1
            df['suggestor_name'] = nan
        else:
            df = pd.read_excel(f, sheetname=target_sheet, header=None, usecols=range(0, 9), skiprows=5, names=['councilor', 'suggestion', 'position', 'suggest_expense', 'approved_expense', 'expend_on', 'brought_by', 'bid_type', 'bid_by'], encoding='utf-8')
            df.dropna(inplace=True, how='any', subset=['suggestion', 'position', 'approved_expense'])
            for key in ['councilor', 'suggestion', 'position', 'suggest_expense', 'brought_by', 'bid_type', 'bid_by']:
                df[key].fillna(inplace=True, method='pad')
            df['suggestor_name'] = df['councilor']
            df['councilor'] = map(lambda x: normalize_person_name(x) if x else nan, df['councilor'])
            df['councilor_ids'] = map(lambda x: getCouncilordetailIdList(common.getCouncilorIdList(c, x), election_year, county) if x else nan, df['councilor'])
            df['councilor_num'] = map(lambda x: len(x) if x else 1, df['councilor_ids'])
    df['election_year'] = election_year
    df['county'] = county
    df['suggest_year'] = meta['year']
    df['suggest_month'] = meta['month_to']
    df['uid'] = map(lambda x: u'{county}-{year}-{month_from}-{month_to}'.format(**meta) + '-%d' % (x+6), df.index)
    df['approved_expense'] = map(lambda x: float(x) if is_number(x) else nan, df['approved_expense'])
    df['suggest_expense'] = map(lambda x: float(x) if is_number(x) else nan, df['suggest_expense'])
    if df['approved_expense'].mean() < 5000.0:
        df['approved_expense'] = map(lambda x: x*1000 if is_number(x) else nan, df['approved_expense'])
        df['suggest_expense'] = map(lambda x: x*1000 if is_number(x) else nan, df['suggest_expense'])
    df['approved_expense_avg'] = df['approved_expense'] / df['councilor_num']
    df['suggest_expense_avg'] = df['suggest_expense'] / df['councilor_num']
    return df

year = 2017
conn = db_settings.con()
c = conn.cursor()

# update suggestions params on councilor
def one_councilor_term_years(data):
    c.execute('''
        SELECT json_build_object('sum', SUM(_.sum), 'count', SUM(_.count), 'years', json_agg(_))
        FROM (
            SELECT suggest_year, COALESCE(SUM(approved_expense_avg), 0) as sum, COALESCE(COUNT(*), 0) as count, SUM(
                CASE
                    WHEN approved_expense <= 100000 THEN 1 ELSE 0
                END
            ) as small_purchase
            FROM suggestions_suggestions s, suggestions_councilors_suggestions sc
            WHERE s.uid = sc.suggestion_id AND sc.councilor_id = %(councilor_id)s
            GROUP BY suggest_year
            ORDER BY suggest_year
        ) _
    ''', data)
    return c.fetchone()[0]

def one_pile_json(data):
    c.execute('''
        SELECT json_build_object('label', %(label)s, 'tokens', %(tokens)s, 'sum', COALESCE(SUM(approved_expense), 0), 'count', COALESCE(COUNT(*), 0))
        FROM suggestions_suggestions s
        WHERE suggestion ~* %(tokens)s OR position ~* %(tokens)s OR brought_by ~* %(tokens)s
    ''', data)
    return c.fetchone()[0]

def one_association_json(token):
    c.execute('''
        SELECT json_build_object('label', %(label)s, 'sum', COALESCE(SUM(approved_expense), 0), 'count', COALESCE(COUNT(*), 0))
        FROM suggestions_suggestions s, suggestions_councilors_suggestions sc
        WHERE s.uid = sc.suggestion_id AND sc.councilor_id = %(councilor_id)s AND (suggestion ~* %(label)s OR position ~* %(label)s OR brought_by ~* %(label)s)
    ''', data)
    return c.fetchone()[0]

piles = []
for pile, tokens in [(u'協會', [u'協會', u'學會', u'商會', u'公會', u'協進會', u'促進會', u'研習會', u'婦聯會', u'婦女會', u'體育會', u'同心會', u'農會', u'早起會', u'健身會', u'宗親會', u'功德會', u'商業會', u'長青會', u'民眾服務社', u'聯盟']), (u'辦公室', [u'辦公室', u'辦公處']), (u'廟', [u'廟', u'宮']), (u'警察局', [u'警察局', u'分局']), (u'消防局', [u'消防局', u'消防隊', u'分隊', u'中隊']), (u'國中、國小', [u'國中', u'國小', u'中學', u'小學'])]:
    data = {
        'label': pile,
        'tokens': u'%s' % u'|'.join(tokens)
    }
    r = one_pile_json(data)
    if r['sum']:
        piles.append(r)
piles = sorted(piles, key=lambda x: x['sum'], reverse=True)
for x in piles:
    print x['label'], x['sum']
