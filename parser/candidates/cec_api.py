#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import os
import json
import requests
import subprocess

import db_settings
import common


refs = {
    u"臺北市": "http://2018.cec.gov.tw/json/candidate/63000.json",
    u"新北市": "http://2018.cec.gov.tw/json/candidate/65000.json",
    u"桃園市": "http://2018.cec.gov.tw/json/candidate/68000.json",
    u"臺中市": "http://2018.cec.gov.tw/json/candidate/66000.json",
    u"臺南市": "http://2018.cec.gov.tw/json/candidate/67000.json",
    u"高雄市": "http://2018.cec.gov.tw/json/candidate/64000.json",
    u"新竹縣": "http://2018.cec.gov.tw/json/candidate/10004.json",
    u"苗栗縣": "http://2018.cec.gov.tw/json/candidate/10005.json",
    u"彰化縣": "http://2018.cec.gov.tw/json/candidate/10007.json",
    u"南投縣": "http://2018.cec.gov.tw/json/candidate/10008.json",
    u"雲林縣": "http://2018.cec.gov.tw/json/candidate/10009.json",
    u"嘉義縣": "http://2018.cec.gov.tw/json/candidate/10010.json",
    u"屏東縣": "http://2018.cec.gov.tw/json/candidate/10013.json",
    u"宜蘭縣": "http://2018.cec.gov.tw/json/candidate/10002.json",
    u"花蓮縣": "http://2018.cec.gov.tw/json/candidate/10015.json",
    u"臺東縣": "http://2018.cec.gov.tw/json/candidate/10014.json",
    u"澎湖縣": "http://2018.cec.gov.tw/json/candidate/10016.json",
    u"金門縣": "http://2018.cec.gov.tw/json/candidate/09020.json",
    u"連江縣": "http://2018.cec.gov.tw/json/candidate/09007.json",
    u"基隆市": "http://2018.cec.gov.tw/json/candidate/10017.json",
    u"新竹市": "http://2018.cec.gov.tw/json/candidate/10018.json",
    u"嘉義市": "http://2018.cec.gov.tw/json/candidate/10020.json"
}

def upsertCandidates(candidate):
    candidate['former_names'] = candidate.get('former_names', [])
    variants = common.make_variants_set(candidate['name'])
    candidate['identifiers'] = list((variants | set(candidate['former_names']) | {candidate['name'], re.sub(u'[\w‧]', '', candidate['name']), re.sub(u'\W', '', candidate['name']).lower(), }) - {''})
    complement = {'birth': None, 'gender': '', 'party': '', 'number': None, 'contact_details': None, 'district': '', 'education': None, 'experience': None, 'remark': None, 'image': '', 'links': None, 'platform': '', 'data': None, 'occupy': None}
    complement.update(candidate)
    c.execute('''
        UPDATE candidates_candidates
        SET birth = %(birth)s
        WHERE uid = %(candidate_uid)s
    ''', complement)
    c.execute('''
        UPDATe candidates_terms
        SET number = %(number)s, name = %(name)s, party = %(party)s, status = %(status)s, education = %(education)s, experience = %(experience)s, platform = %(platform)s, gender = %(gender)s, image = COALESCE(nullif(candidates_terms.image,''), %(image)s), data = (COALESCE(data, '{}'::jsonb) || %(cec_data)s)
        WHERE election_year = %(election_year)s AND candidate_id = %(candidate_uid)s
    ''', complement)

conn = db_settings.con()
c = conn.cursor()
election_year = '2018'

for county, url in refs.items():
    rows = requests.get(url).json()
    for row in rows:
        if re.search('(20182020001|20183020001)', row['ElectionId']):
            position_type = 'councilors'
        elif re.search('(20182010001|20183010001)', row['ElectionId']):
            position_type = 'mayors'
        else:
            continue
        path = '../../data/avatar/candidates/%s/%s' % (position_type, election_year, )
        subprocess.call('mkdir -p %s' % path, shell=True)
        candidate = {}
        candidate['type'] = position_type
        candidate['status'] = 'approved'
        candidate['county'] = county
        if candidate['type'] == 'councilors':
            match = re.search(u'第(?P<num>\d+)選(?:舉)?區', row['DistrictName'])
            candidate['constituency'] = match.group('num')
        else:
            candidate['constituency'] = 0
        candidate['name'] = common.normalize_person_name(row['CandidateName'])
        print candidate['name'], candidate['county'], candidate['constituency']
        party = re.sub(u'無政?黨?$', u'無黨籍', row['EndorsementPartyName1'])
        candidate['party'] = party
        candidate['election_year'] = election_year
        candidate['birth'] = '%s-%s-%s' % (row['DateOfBirth'][:4],row['DateOfBirth'][4:6],row['DateOfBirth'][6:], )
        candidate['number'] = row['DrawNo']
        candidate['gender'] = row['Gender']
        candidate['education'] = row['BulletinEducation']
        candidate['experience'] = row['BulletinExperience']
        candidate['platform'] = row['BulletinPlatform']
        f_name = '%s_%d_%04d' % (candidate['county'], int(candidate['constituency']), int(candidate['number']), )
        if re.search('^data:image', row['src']):
            _, encode_data = row['src'].split(',') # [sic]
            ext = re.search('data:image/(\w+);', _).group(1)
            code = _.split(';')[-1]
            f_name = '%s.%s' % (f_name, ext)
            f = '%s/%s' % (path, f_name)
            if not os.path.isfile(f):
                with open(f, 'wb') as img_file:
                    img_file.write(encode_data.decode(code))
        else:
            candidate['image'] = 'https://www.cec.gov.tw/json/candidatepic/%s' % re.sub('\\\\', '/', row['src'])
            ext = row['src'].split('.')[-1]
            f_name = '%s.%s' % (f_name, ext)
            f = '%s/%s' % (path, f_name)
            if not os.path.isfile(f):
                cmd = 'wget --no-check-certificate "%s" -O %s' % (candidate['image'], f)
                subprocess.call(cmd, shell=True)
        candidate['image'] = u'%s/candidates/%s/%s/%s' % (common.storage_domain(), position_type, election_year, f_name)
        if candidate['type'] == 'mayors':
            candidate['candidate_uid'], created = common.get_or_create_moyor_candidate_uid(c, candidate, create=False)
        else:
            candidate['candidate_uid'], created = common.get_or_create_candidate_uid(c, candidate, create=False)
        row['image'] = candidate['image']
        candidate['cec_data'] = {'cec_data': row}
        candidate['candidate_term_uid'] = '%s-%s' % (candidate['candidate_uid'], election_year)
        upsertCandidates(candidate)
conn.commit()
