#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../../')
import re
import codecs
import unicodedata
import json
import psycopg2
import db_settings
import common


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
election_years = {1: '2010', 2: '2014'}
election_year = '2010'
county, county_abbreviation = u'新北市', u'TPQ'

Session_Token = re.compile(u'''
    (?P<name>
        第(?P<ad>\d+)屆
        第(?P<session>\d+)次(?P<type>(定期|臨時))大?會
    )
''', re.X)

Present_Token = re.compile(u'''
    出\s*席[:：]?
    (?P<names>.+?)
    (請\s*假.*?)?
    列\s*席
''', re.X|re.S)

meetings = json.load(open('../../../data/ntcc/meeting_minutes-%s.json' % election_year))
for meeting in meetings:
    total_text = unicodedata.normalize('NFC', codecs.open('../../../data/ntcc/meeting_minutes/%s_%s.txt' % (meeting['sitting'], meeting['meeting']), "r", "utf-8").read())
    total_text = re.sub(u'．', u'‧', total_text)
    total_text = re.sub(u'　', ' ', total_text)
    match = Session_Token.search(meeting['sitting'])
    if match:
        if match.group('type') == u'定期':
            uid = '%s-%s-%02d-CS-%02d' % (county_abbreviation, election_years[int(match.group('ad'))], int(match.group('session')), int(meeting['meeting']))
        elif match.group('type') == u'臨時':
            uid = '%s-%s-T%02d-CS-%02d' % (county_abbreviation, election_years[int(match.group('ad'))], int(match.group('session')), int(meeting['meeting']))
        sitting = {"uid": uid, "name": u'%s議會%s第%s會議' % (county, meeting['sitting'], meeting['meeting']), "county": county, "election_year": election_years[int(match.group('ad'))], "session": match.group('session'), "date": meeting['date']}
    # --> sittings, attendance, filelog
    print sitting
    common.InsertSitting(c, sitting)
    common.FileLog(c, sitting['name'])
    # present
    present_match = Present_Token.search(total_text)
    exclude = []
    if present_match:
        names = re.sub(u'(副?議長|議員)', '', present_match.group('names'))
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
conn.commit()
print 'votes, voter done!'
