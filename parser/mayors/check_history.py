#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import uuid
import json
import glob
from datetime import datetime

import pandas as pd

from common import ly_common
from common import db_settings


conn = db_settings.con()
c = conn.cursor()
ad = 9
try:
    con_another = db_settings.con_another()
    c_another = con_another.cursor()
    c.execute('''
        SELECT name
        FROM candidates_terms
        WHERE ad = %s
    ''', (ad, ))
    r = [x[0] for x in c.fetchall()]
    c_another.execute('''
        SELECT json_agg(row)
        FROM (
            SELECT name, county, constituency, councilor_id, last_election_year, elected
            FROM candidates_candidates
            WHERE name IN %s
        ) row
    ''', (tuple(r), ))
    r_another = c_another.fetchone()[0]
    for legislator_candidate in r:
        m = re.match(u'(?P<cht>.+?)[a-zA-Z]', legislator_candidate)
        if m:
            name_like = '%s%%' % m.group('cht')
        else:
            continue
        c_another.execute('''
            SELECT json_agg(row)
            FROM (
                SELECT name, county, constituency, councilor_id, last_election_year, elected
                FROM candidates_candidates
                WHERE name like %s
            ) row
        ''', (name_like, ))
        liked = c_another.fetchone()
        if liked[0]:
            r_another.append(liked[0][0])
    with open('candidates/%s/cross.json' % ad, 'w') as outfile:
        json.dump(r_another, outfile)
except:
    with open('candidates/%s/cross.json' % ad, 'r') as infile:
        r_another = json.load(infile)
finally:
    for councilor_candidate in r_another:
        c.execute('''
            UPDATE candidates_terms
            SET councilor = %s
            WHERE name = %s
        ''', (councilor_candidate, councilor_candidate['name']))
    conn.commit()

