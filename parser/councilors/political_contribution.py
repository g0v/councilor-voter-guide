#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import glob
import json
import db_settings
import common


def PoliticalContributions(data_set):
    try:
        c.execute('''
            UPDATE councilors_politicalcontributions
            SET in_individual = %(in_individual)s, in_profit = %(in_profit)s, in_party = %(in_party)s, in_civil = %(in_civil)s, in_anonymous = %(in_anonymous)s, in_others = %(in_others)s, in_total = %(in_total)s, out_personnel = %(out_personnel)s, out_propagate = %(out_propagate)s, out_campaign_vehicle = %(out_campaign_vehicle)s, out_campaign_office = %(out_campaign_office)s, out_rally = %(out_rally)s, out_travel = %(out_travel)s, out_miscellaneous = %(out_miscellaneous)s, out_return = %(out_return)s, out_exchequer = %(out_exchequer)s, out_public_relation = %(out_public_relation)s, out_total = %(out_total)s, balance = %(balance)s
            WHERE councilor_id = %(councilor_id)s
        ''', data_set)
        c.execute('''
            INSERT into councilors_politicalcontributions(councilor_id, in_individual, in_profit, in_party, in_civil, in_anonymous, in_others, in_total, out_personnel, out_propagate, out_campaign_vehicle, out_campaign_office, out_rally, out_travel, out_miscellaneous, out_return, out_exchequer, out_public_relation, out_total, balance)
            SELECT %(councilor_id)s, %(in_individual)s, %(in_profit)s, %(in_party)s, %(in_civil)s, %(in_anonymous)s, %(in_others)s, %(in_total)s, %(out_personnel)s, %(out_propagate)s, %(out_campaign_vehicle)s, %(out_campaign_office)s, %(out_rally)s, %(out_travel)s, %(out_miscellaneous)s, %(out_return)s, %(out_exchequer)s, %(out_public_relation)s, %(out_total)s, %(balance)s
            WHERE NOT EXISTS (SELECT 1 FROM councilors_politicalcontributions WHERE councilor_id = %(councilor_id)s)
        ''', data_set)
    except Exception, e:
        print data_set
        raise

conn = db_settings.con()
c = conn.cursor()
for f in glob.glob('../../data/political_contribution/*.json'):
    dict_list = json.load(open(f))
    for candidate in dict_list:
        for wrong, right in [(u'涂淑媚', u'凃淑媚')]:
            candidate['name'] = re.sub(wrong, right, candidate['name'])
        candidate['councilor_id'] = common.getDetailId(c, candidate['name'], candidate['election_year'], candidate['county'])
        if candidate['councilor_id']:
            PoliticalContributions(candidate)
conn.commit()
