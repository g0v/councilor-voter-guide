#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import os
import json
import glob
import requests
import subprocess

import db_settings
import common


def upsertCandidates(candidate):
    c.execute('''
        UPDATe candidates_terms
        SET votes = %(votes)s, votes_percentage = %(votes_percentage)s, elected = %(elected)s
        WHERE election_year = %(election_year)s AND county = %(county)s AND constituency = %(constituency)s AND number = %(number)s
    ''', candidate)

conn = db_settings.con()
c = conn.cursor()
election_year = '2018'

for category in ['mayors', 'councilors']:
    rows = json.load(open('../../data/candidates/%s/%s.json' % (election_year, category)))
    for row in rows:
        row['election_year'] = election_year
        row['elected'] = True if re.search(u'[*!]', row['elected']) else None
        upsertCandidates(row)
conn.commit()
