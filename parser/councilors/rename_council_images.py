#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
import subprocess
import urllib

import db_settings
import common


conn = db_settings.con_middle2()
c = conn.cursor()
election_year = '2014'
path = '../../data/avatar/councilors/%s' % election_year
cmd = 'mkdir -p %s' % path
subprocess.call(cmd, shell=True)
c.execute('''
    SELECT id, county, constituency, name, image
    FROM councilors_councilorsdetail
    WHERE election_year = %s AND image != ''
    ORDER BY county
''', [election_year])

key = [desc[0] for desc in c.description]
for person in c.fetchall():
    person = dict(zip(key, person))
    f_name = '%s_%d_%s' % (person['county'], person['constituency'], person['name'])
    f = '%s/%s' % (path, f_name)
    if not os.path.isfile(f):
        cmd = 'wget --no-check-certificate "%s" -O %s' % (person['image'], f)
        subprocess.call(cmd, shell=True)
    image_url = '%s/%s/%s/%s' % (common.storage_domain(), 'councilors', election_year, f_name)
    c.execute('''
        UPDATE candidates_terms
        SET image = %s
        WHERE elected_councilor_id = %s
    ''', [image_url, person['id']])
conn.commit()
