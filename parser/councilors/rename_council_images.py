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


conn = db_settings.con()
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
    print person['name']
    f_name = '%s_%d_%s' % (person['county'], person['constituency'], person['name'])
    f = '%s/%s' % (path, f_name)
    cmd = 'wget -N --no-check-certificate --header="User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36" "%s" -O %s' % (person['image'], f)
    subprocess.call(cmd, shell=True)
    image_url = '%s/%s/%s/%s' % (common.storage_domain(), 'councilors', election_year, f_name)
    if os.path.isfile(f):
        c.execute('''
            UPDATE candidates_terms
            SET image = %s
            WHERE elected_councilor_id = %s
        ''', [image_url, person['id']])
conn.commit()
