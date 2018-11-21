#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import db_settings
import common


conn = db_settings.con()
c = conn.cursor()
election_year = '2018'

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credential.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_key('1yK3rw5mgW_kbu02NEl65huwhNML4eFpMMjPJSfEf-PY')
worksheets = sh.worksheets()
referenda = []
for wks in worksheets:
    rows = wks.get_all_records()
    for row in rows:
        fragment = {}
        if not row[u'理由書連結']:
            continue
        fragment['serial_number'] = row[u'序號']
        fragment['number'] = row[u'案號']
        fragment['proposal_date'] = common.ROC2AD(row[u'提案日期'])
        fragment['title'] = row[u'主文']
        fragment['proposer'] = row[u'領銜人']
        fragment['status'] = row[u'最新受理進度']
        fragment['cec_file_link'] = row[u'理由書連結']
        fragment['cec_page_link'] = row[u'中選會連結']
        fragment['uid'] = row[u'中選會連結'].split('/')[-1]
        referenda.append(fragment)
    referenda = sorted(referenda, key=lambda x: int(x['number']))
config = json.dumps({'referenda': referenda})
c.execute('''
    INSERT INTO elections_elections(id, data)
    VALUES (%s, %s)
    ON CONFLICT (id)
    DO UPDATE
    SET data = (COALESCE(elections_elections.data, '{}'::jsonb) || %s::jsonb)
''', [election_year, config, config])
conn.commit()
