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
county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
county = common.county_abbr2string(county_abbr)
election_year = common.election_year(county)
county_abbr3 = common.county2abbr3(county)

Session_Token = re.compile(u'''
    (?P<name>
        屆第(?P<session>\W{1,3})次(?P<type>(定期|臨時))大?會
    )
''', re.X)

Present_Token = re.compile(u'''
    出席議員[:：]
    (?P<names>.+?)
    (?=(計\d+位|請假|列席))
''', re.X|re.S)

meetings = json.load(open('../../../data/kmc/meeting_minutes-%s.json' % election_year))
for meeting in meetings:
    total_text = unicodedata.normalize('NFC', codecs.open('../../../data/kmc/meeting_minutes/%s/%s.txt' % (election_year, meeting['sitting']), "r", "utf-8").read())
    total_text = re.sub(u'．', u'‧', total_text)
    total_text = re.sub(u'　', ' ', total_text)
    match = Session_Token.search(meeting['sitting'])
    if match:
        for i, session in enumerate(Present_Token.finditer(total_text), 1):
            meeting['date'] = common.ROC2AD(re.search(u'時\s*間[:：](.*)', total_text[:session.start()].strip().split('\n')[-1]).group(1))
            if match.group('type') == u'臨時':
                uid = '%s-%s-T%s-CS-%02d' % (county_abbr3, election_year, match.group('session'), i)
            else:
                uid = '%s-%s-%s-CS-%02d' % (county_abbr3, election_year, match.group('session'), i)
            sitting = {"uid": uid, "name": u'%s議會%s第%d次會議' % (county, meeting['sitting'], i), "county": county, "election_year": election_year, "session": match.group('session'), "date": meeting['date']}
            # --> sittings, attendance, filelog
            print sitting
            common.InsertSitting(c, sitting)
            common.FileLog(c, sitting['name'])
            # present
            exclude = []
            names = re.sub(u'(副?議長|議員)', '', session.group('names'))
            names = re.sub(u'\s', '', names)
            names = re.sub(u'、', ' ', names)
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

vote_common.not_attend_complement(c, county)
vote_common.person_attendance_param(c, county)
conn.commit()
print 'Succeed'
