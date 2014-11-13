#!/usr/bin/python
# -*- coding: utf-8 -*
import re
import glob
import json
import codecs
import pandas as pd
from numpy import nan


def AD2AD(text):
    matchTerm = re.search(u'''
        (?P<year>[\d]+)[\s]*(年|[./-])[\s]*
        (?P<month>[\d]+)[\s]*(月|[./-])[\s]*
        (?P<day>[\d]+)
    ''', text, re.X)
    if matchTerm:
        return '%04d-%02d-%02d' % (int(matchTerm.group('year')), int(matchTerm.group('month')), int(matchTerm.group('day')))
    else:
        return None

def write_file(data, file_name):
    file = codecs.open(file_name, 'w', encoding='utf-8')
    file.write(data)
    file.close()

df_concat = pd.DataFrame()
for i in range(1, 8):
    df = pd.read_excel('ntcc/councilors.xlsx', sheetname=u'第%d選區' % i, skiprows=1, header=None, usecols=range(1, 13), names=['name', 'education', 'image', 'contact_details', 'title', 'birth', 'gender', 'birth_place', 'district', 'party', 'experience', 'platform'], parse_dates='birth', encoding='utf-8')
    print i
    df['constituency'] = u'第%d選區' % i
    df_concat = pd.concat([df_concat, df])
df_concat['election_year'] = '2009'
df_concat['county'] = u'南投縣'
df_concat['term_start'] = '2009-12-25'
df_concat['in_office'] = True
df_concat['title'].fillna(u'議員', inplace=True)
df_concat['birth'] = map(lambda x: AD2AD(str(x)) if x else [], df_concat['birth'])
df_concat['contact_details'] = map(lambda x: [{'type': 'address', 'label': u'通訊處', 'value': x}] if x else nan, df_concat['contact_details'])
for key in ['education', 'experience', 'platform']:
    df_concat[key] = map(lambda x: x.split('\n') if isinstance(x, basestring) else [], df_concat[key])
ds = json.loads(df_concat.to_json(orient='records', force_ascii=False))
for d in ds:
    d['term_end'] = {'date': '2014-12-25'}
dump_data = json.dumps(ds, sort_keys=True, ensure_ascii=False)
write_file(dump_data, 'ntcc/councilors.json')
dump_data = json.dumps(ds, sort_keys=True, indent=4, ensure_ascii=False)
write_file(dump_data, 'pretty_format/ntcc/councilors.json')
