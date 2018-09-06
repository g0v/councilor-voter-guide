#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import glob
import json
import db_settings
import common
import logging


logging.basicConfig(filename='pc.log', level=logging.ERROR)

def PoliticalContributions(data):
    '''
    Store political contrbution history to candidate, e.g. all record before 2018(<=) will store into candidate which election_year less than 2018(<=)
    '''

    c.execute('''
        UPDATE candidates_terms
        SET politicalcontributions = COALESCE(politicalcontributions, '[]'::jsonb) || %(politicalcontributions)s::jsonb
        WHERE candidate_id = %(candidate_uid)s AND election_year >= %(election_year)s
    ''', data)
    c.execute('''
        UPDATE candidates_terms
        SET politicalcontributions = (SELECT jsonb_agg(x) FROM (
            SELECT x from (
                SELECT DISTINCT(value) as x
                FROM jsonb_array_elements(politicalcontributions)
                WHERE value->'title' is not null
            ) t ORDER BY x->'election_year' DESC
        ) tt)
        WHERE candidate_id = %(candidate_uid)s AND election_year >= %(election_year)s
    ''', data)

conn = db_settings.con()
c = conn.cursor()
for f in glob.glob('../../data/political_contribution/*.json'):
    dict_list = json.load(open(f))
    for candidate in dict_list:
        if not candidate['name']:
            continue
        for wrong, right in [(u'涂淑媚', u'凃淑媚')]:
            candidate['name'] = re.sub(wrong, right, candidate['name'])
        income = {key: candidate[key] for key in ["in_individual", "in_profit", "in_party", "in_civil", "in_anonymous", "in_others"]}
        expenses = {key: candidate[key] for key in ["out_personnel", "out_propagate", "out_campaign_vehicle", "out_campaign_office", "out_rally", "out_travel", "out_miscellaneous", "out_return", "out_exchequer", "out_public_relation"]}
        pc = {key: candidate[key] for key in ["in_total", "out_total", "balance"]}
        pc.update({'in': income, 'out': expenses})
        pc = [{
            'election_year': candidate['election_year'],
            'title': candidate.get('title', 'councilors'),
            'election_name': candidate.get('election_name', u'%s議員選舉' % candidate['county']),
            'pc': pc
        }]
        candidate['politicalcontributions'] = json.dumps(pc)
        candidate['name'] = common.normalize_person_name(candidate['name'])
        candidate['constituency'] = None
        candidate['candidate_uid'], created = common.get_or_create_candidate_uid(c, candidate, create=False)
        if not candidate['candidate_uid'] and candidate.get('title', '') == 'mayors':
            candidate['candidate_uid'], created = common.get_or_create_moyor_candidate_uid(c, candidate)
        if candidate['candidate_uid']:
            PoliticalContributions(candidate)
        else:
            logging.error(u'not exist candidate: %s, %s' % (candidate['name'], candidate['election_year']))
conn.commit()
