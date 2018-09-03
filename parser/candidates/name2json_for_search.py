#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import codecs
import os
import json

import db_settings


conn = db_settings.con()
c = conn.cursor()
election_year = '2018'

c.execute('''
    SELECT json_agg(_.name)
    FROM (
        SELECT name, county, constituency
        FROM candidates_terms
        WHERE election_year = %s and status = 'register'
        ORDER BY name, county, constituency
    ) _
''', [election_year, ])
rows = c.fetchone()
f_out = '../../voter_guide/static/json/dest/candidates_names_%s.json' % election_year
json.dump(rows[0], codecs.open(f_out, 'w', 'utf-8'), ensure_ascii=False)
