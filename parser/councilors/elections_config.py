#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import json
import psycopg2

import db_settings


conn = db_settings.con()
c = conn.cursor()
election_year = '2018'
county_versions = json.load(open('../county_versions.json'))
district_versions = json.load(open('../district_versions.json'))
config = json.dumps({'constituency_change': district_versions[election_year]})
c.execute('''

    INSERT INTO elections_elections(id, data)
    VALUES (%s, %s)
    ON CONFLICT (id)
    DO UPDATE
    SET data = (COALESCE(elections_elections.data, '{}'::jsonb) || %s::jsonb)
''', [election_year, config, config])
conn.commit()
