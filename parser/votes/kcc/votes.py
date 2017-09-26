#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../../')
import os
import re
import codecs
import unicodedata
import json
import glob
import psycopg2

import db_settings
import common
import vote_common


def UpsertVote(data):
    c.execute('''
        UPDATE votes_votes
        SET sitting_id = %(sitting_id)s, date = %(date)s, vote_seq = %(vote_seq)s, content = %(content)s, conflict = null
        WHERE uid = %(uid)s
    ''', data)
    c.execute('''
        INSERT INTO votes_votes(uid, sitting_id, date, vote_seq, content)
        SELECT %(uid)s, %(sitting_id)s, %(date)s, %(vote_seq)s, %(content)s
        WHERE NOT EXISTS (SELECT 1 FROM votes_votes WHERE uid = %(uid)s)
    ''', data)

def VoteVoterRelation(councilor_id, vote_id, decision):
    c.execute('''
        UPDATE votes_councilors_votes
        SET decision = %s, conflict = null
        WHERE councilor_id = %s AND vote_id = %s
    ''', (decision, councilor_id, vote_id))
    c.execute('''
        INSERT INTO votes_councilors_votes(councilor_id, vote_id, decision)
        SELECT %s, %s, %s
        WHERE NOT EXISTS (SELECT 1 FROM votes_councilors_votes WHERE councilor_id = %s AND vote_id = %s)
    ''',(councilor_id, vote_id, decision, councilor_id, vote_id))

def IterVote(text, sitting_dict):
    print sitting_dict["uid"]
    vote_count = 1
    pre_match_end = 0
    for match in Namelist_Token.finditer(text):
        vote_seq = str(vote_count).zfill(3)
        vote_dict = {'uid': '%s-%s' % (sitting_dict["uid"], vote_seq), 'sitting_id': sitting_dict["uid"], 'vote_seq': vote_seq, 'date': sitting_dict["date"], 'content': match.group()}
        UpsertVote(vote_dict)
        ref = {u'贊成': 1, u'反對': -1, u'棄權': 0}
        for key, value in ref.items():
            for i in range(0, len(match.groups()), 2):
                if match.groups()[i] == key:
                    names = re.sub(u'(副?議長|議員)', '', match.groups()[i+1])
                    for id, councilor_id in common.getIdList(c, common.getNameList(re.sub(u'[、：，:,]', ' ', names)), sitting_dict):
                        VoteVoterRelation(id, vote_dict['uid'], value)
        vote_count += 1
        pre_match_end = match.end()

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
county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
county = common.county_abbr2string(county_abbr)
election_year = common.election_year(county)
county_abbr3 = common.county2abbr3(county)

total_text = unicodedata.normalize('NFC', codecs.open(u"../../../data/kcc/meeting_minutes-%s.txt" % election_year, "r", "utf-8").read())
meetings = json.load(open('../../../data/kcc/meeting_minutes-%s.json' % election_year))
total_text = re.sub(u'．', u'‧', total_text)

Session_Token = re.compile(u'''
    \s*
    (?P<name>
        %s議會
        第\s*(?P<ad>[\d]+)\s*屆
        第\s*(?P<session>[\d]+)\s*次(?P<type>(定期|臨時))大?會
        (預備會議暨)?
        第\s*(?P<times>[\d]+)\s*次
        會議
    )
    紀錄
''' % county, re.X)

Absent_Token = re.compile(u'''
    請\s*假[:：]
    (?P<names>.+?)
    \s*列\s*席
''', re.X|re.S)

Namelist_Token = re.compile(u'''
    ^.*?
    具名表決[，,]
    (贊成|反對).*?者有(?P<dicision_a>.*)[，,]?共計\s*\d+位[；;]
    (贊成|反對).*?者有(?P<dicision_b>.*)[，,]?共計\s*\d+位[；;]
    表決結果.*?$
''', re.X | re.M)

sittings = []
for match in Session_Token.finditer(total_text):
    if match:
        if match.group('type') == u'定期':
            uid = '%s-%s-%02d-CS-%02d' % (county_abbr3, election_years[int(match.group('ad'))], int(match.group('session')), int(match.group('times')))
        elif match.group('type') == u'臨時':
            uid = '%s-%s-T%02d-CS-%02d' % (county_abbr3, election_years[int(match.group('ad'))], int(match.group('session')), int(match.group('times')))
        sittings.append({"uid":uid, "name": re.sub('\s', '', match.group('name')), "county": county, "election_year": election_years[int(match.group('ad'))], "session": match.group('session'), "date": common.ROC2AD(total_text[match.end():]), "start": match.start(), "end": match.end()})
for i in range(0, len(sittings)):
    # --> sittings, attendance, filelog
    if i != len(sittings)-1:
        one_sitting_text = total_text[sittings[i]['start']:sittings[i+1]['start']]
    else:
        one_sitting_text = total_text[sittings[i]['start']:]
    print sittings[i]
    common.InsertSitting(c, sittings[i])
    common.FileLog(c, sittings[i]['name'])
    # absent
    absent_match = Absent_Token.search(one_sitting_text)
    exclude = []
    if absent_match:
        names = re.sub(u'(副?議長|議員)計?', u'、', absent_match.group('names'))
        names = re.sub(u'\n', '', names)
        names = re.sub(u'、', ' ', names)
        names = re.sub(u'([^(（]*)[(（][^)）]+[)）]', u'\g<1>', names)
        if names:
            exclude = common.Attendance(c, sittings[i], names, 'CS', 'absent')
        else:
            print one_sitting_text
            raise
    # present
    for councilor_id in in_office_ids(sittings[i]['date'], exclude):
        common.AddAttendanceRecord(c, councilor_id, sittings[i]['uid'], 'CS', 'present')
    # <--
    # --> votes
#   IterVote(one_sitting_text, sittings[i])
    # <--
conn.commit()
print 'votes, voter done!'

print 'update meeting_minutes download links'
meetings = json.load(open('../../../data/kcc/meeting_minutes-%s.json' % election_year))
for meeting in meetings:
    meeting['county'] = county
    meeting['links'] = {'url': meeting['download_url'], 'note': u'議會官網會議紀錄'}
    meeting['name'] = re.sub(u'第0+', u'第', u'%s議會%s' % (meeting['county'], meeting['meeting']))
    meeting['name'] = re.sub(u'紀錄.*$', '', meeting['name'])
    print meeting['name']
    common.UpdateSittingLinks(c, meeting)
print 'done!'

vote_common.conscience_vote(c, election_year, county)
vote_common.not_voting_and_results(c, county)
vote_common.person_vote_param(c, county)
vote_common.person_attendance_param(c, county)
conn.commit()
print 'Succeed'
