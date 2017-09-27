#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../../')
import os
import re
import codecs
import unicodedata
import json
import psycopg2

import db_settings
import common
import vote_common


def in_office_ids(date, exclude):
    if exclude:
        c.execute('''
            select id
            from councilors_councilorsdetail
            where election_year = %s and county = %s and term_start <= %s and cast(term_end::json->>'date' as date) > %s and id not in %s
        ''', (election_year, county, date, date, tuple(exclude)))
    else:
        c.execute('''
            select id
            from councilors_councilorsdetail
            where election_year = %s and county = %s and term_start <= %s and cast(term_end::json->>'date' as date) > %s
        ''', (election_year, county, date, date))
    return c.fetchall()

conn = db_settings.con()
c = conn.cursor()
election_years = {1: '2010', 2: '2014', 3: '2018'}
county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
county = common.county_abbr2string(county_abbr)
election_year = common.election_year(county)
county_abbr3 = common.county2abbr3(county)

Session_Token = re.compile(u'''
    (?P<name>
        第(?P<session>\d+)次(?P<type>(臨時))?大?會
    )
''', re.X)

Present_Token = re.compile(u'''
    出席議員[:：]
    (?P<names>.+?)
    (?=(計\d+位|請假|列席))
''', re.X|re.S)

meetings = json.load(open('../../../data/ilcc/meeting_minutes-%s.json' % election_year))
for meeting in meetings:
    total_text = unicodedata.normalize('NFC', codecs.open('../../../data/ilcc/meeting_minutes/%s/%s_%s.txt' % (election_year, meeting['sitting'], meeting['meeting']), "r", "utf-8").read())
    total_text = re.sub(u'．', u'‧', total_text)
    total_text = re.sub(u'　', ' ', total_text)
    match = Session_Token.search(meeting['sitting'])
    if match:
        if match.group('type') == u'臨時':
            uid = '%s-%s-T%02d-CS-%02d' % (county_abbr3, election_year, int(match.group('session')), int(re.sub('\D', '', meeting['meeting'])))
        else:
            uid = '%s-%s-%02d-CS-%02d' % (county_abbr3, election_year, int(match.group('session')), int(re.sub('\D', '', meeting['meeting'])))
        sitting = {"uid": uid, "name": u'%s議會%s%s' % (county, meeting['sitting'], meeting['meeting']), "county": county, "election_year": election_year, "session": match.group('session'), "date": meeting['date']}
    # --> sittings, attendance, filelog
    print sitting
    common.InsertSitting(c, sitting)
    common.FileLog(c, sitting['name'])
    # present
    present_match = Present_Token.search(total_text)
    exclude = []
    if present_match:
        names = re.sub(u'(副?議長|議員)', '', present_match.group('names'))
        print names
        if names:
            exclude.extend(common.Attendance(c, sitting, names, 'CS', 'present'))
        else:
            print total_text
            raise
    # no councilor's name to record
    if exclude == []:
        continue
    # absent
    for councilor_id in in_office_ids(sitting['date'], exclude):
        common.AddAttendanceRecord(c, councilor_id, sitting['uid'], 'CS', 'absent')
    # <--
print 'votes, voter done!'

vote_common.person_attendance_param(c, county)
conn.commit()
print 'Succeed'
