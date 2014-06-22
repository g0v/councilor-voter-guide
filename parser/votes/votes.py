#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import re
import codecs
import json
import glob
import psycopg2
from datetime import datetime
import db_settings
import common


def InsertVote(uid, sitting_id, vote_seq, content):
    match = re.search(u'(?:建請|建請決議|並請|提請|擬請|要求)(?:\S){0,4}(?:院會|本院|\W{1,3}院|\W{1,3}部|\W{1,3}府).*(?:請公決案|敬請公決)', content)
    summary = ''
    if match:
        summary = match.group()
    c.execute('''
        UPDATE vote_vote
        SET summary = %s
        WHERE uid = %s
    ''', (summary, uid))
    #c.execute('''
    #    UPDATE vote_vote
    #    SET content = %s, conflict = null
    #    WHERE uid = %s
    #''', (content, uid))
    c.execute('''
        INSERT into vote_vote(uid, sitting_id, vote_seq, content, summary, hits, likes, dislikes)
        SELECT %s, %s, %s, %s, %s, 0, 0, 0
        WHERE NOT EXISTS (SELECT 1 FROM vote_vote WHERE uid = %s)
    ''', (uid, sitting_id, vote_seq, content, summary, uid))

def GetVoteContent(c, vote_seq, text):
    l = text.split()
    if re.search(u'附後\S[\d]+\S', l[-2]) or re.search(u'^(其他事項|討論事項)$', l[-2]):
        return l[-1]
    if re.search(u'[：:]$', l[-2]) or re.search(u'(公決|照案|議案)[\S]{0,3}$', l[-2]) or re.search(u'^(決議|決定)[：:]', l[-1]):
        return '\n'.join(l[-2:])
    if re.search(u'[：:]$',l[-3]):
        return '\n'.join(l[-3:])
    i = -3
    # 法條修正提案列表類
    if ly_common.GetLegislatorId(c, l[-2]) or ly_common.GetLegislatorId(c, l[-3]) or re.search(u'(案|審查)[\S]{0,3}$', l[-2]):
        while not re.search(u'(通過|附表|如下)[\S]{1,2}$', l[i]):
            i -= 1
        return '\n'.join(l[i:])
    # 剩下的先向上找上一個附後，找兩附後之間以冒號作結，如找不到
    if vote_seq != '001':
        while not re.search(u'附後\S[\d]+\S', l[i]):
            i -= 1
        for line in reversed(range(i-1,-3)):
            if re.search(u'[：:]$', l[line]):
                return '\n'.join(l[line:])
        return '\n'.join(l[i+1:])
    # 最後方法
    if re.search(u'^[\S]{1,5}在場委員', l[-1]):
        return '\n'.join(l[-2:])
    else:
        return l[-1]
    print l[-1]

def MakeVoteRelation(legislator_id, vote_id, decision):
    c.execute('''
        UPDATE vote_legislator_vote
        SET decision = %s, conflict = null
        WHERE legislator_id = %s AND vote_id = %s
    ''', (decision, legislator_id, vote_id))
    c.execute('''
        INSERT into vote_legislator_vote(legislator_id, vote_id, decision)
        SELECT %s, %s, %s
        WHERE NOT EXISTS (SELECT 1 FROM vote_legislator_vote WHERE legislator_id = %s AND vote_id = %s)
    ''',(legislator_id, vote_id, decision, legislator_id, vote_id))

def LiterateVoter(c, sitting_dict, text, vote_id, decision):
    firstName = ''
    for name in text.split():
        #--> 兩個字的立委中文名字中間有空白
        if len(name) < 2 and firstName == '':
            firstName = name
            continue
        if len(name) < 2 and firstName != '':
            name = firstName + name
            firstName = ''
        #<--
        legislator_id = ly_common.GetLegislatorId(c, name)
        if legislator_id:
            legislator_id = ly_common.GetLegislatorDetailId(c, legislator_id, sitting_dict["ad"])
            MakeVoteRelation(legislator_id, vote_id, decision)
        else:
            print 'break at: %s' % name
            break

def IterEachDecision(c, votertext, sitting_dict, vote_id):
    mapprove, mreject, mquit = re.search(u'\s贊成[\S]*?者[:：][\d]+人', votertext), re.search(u'\s反對[\S]*?者[:：][\d]+人', votertext), re.search(u'棄權者[:：][\d]+人', votertext)
    if not mapprove:
        print u'==找不到贊成者==\n', votertext
    else:
        LiterateVoter(c, sitting_dict, votertext[mapprove.end():], vote_id, 1)
    if not mreject:
        print u'==找不到反對者==\n', votertext
    else:
        LiterateVoter(c, sitting_dict, votertext[mreject.end():], vote_id, -1)
    if not mquit:
        print u'==找不到棄權者==\n', votertext
    else:
        LiterateVoter(c, sitting_dict, votertext[mquit.end():], vote_id, 0)
    return mapprove, mreject, mquit

def IterVote(c, text, sitting_dict):
    sitting_id = sitting_dict["uid"]
    print sitting_id
    match, vote_id, vote_seq = None, None, '000'
    # For normal voting
    mvoter = re.search(u'記名表決結果名單[:：]', text)
    if mvoter:
        votertext = text[mvoter.end():]
        for match in re.finditer(u'附後[（(】。](?P<vote_seq>[\d]+)?', text):
            if match.group('vote_seq'):
                vote_seq = '%03d' % int(match.group('vote_seq'))
            else:
                vote_seq = '001'
            vote_id = '%s-%s' % (sitting_id, vote_seq)
            content = GetVoteContent(c, vote_seq, text[:match.start()+2])
            if content:
                InsertVote(vote_id, sitting_id, vote_seq, content)
            if vote_id:
                mapprove, mreject, mquit = IterEachDecision(c, votertext, sitting_dict, vote_id)
            votertext = votertext[(mquit or mreject or mapprove).end():]
        if not match:
            print u'有記名表決結果名單無附後'
    else:
        print u'無記名表決結果名單'
    # For veto or no-confidence voting
    mvoter = re.search(u'記名投票表決結果[:：]', text)
    if mvoter:
        print u'有特殊表決!!\n'
        votertext = text[mvoter.end():]
        vote_seq = '%03d' % (int(vote_seq)+1)
        vote_id = '%s-%s' % (sitting_id, vote_seq)
        content = GetVoteContent(c, vote_seq, text[:mvoter.start()])
        if content:
            InsertVote(vote_id, sitting_id, vote_seq, content)
        if vote_id:
            mapprove, mreject, mquit = IterEachDecision(c, votertext, sitting_dict, vote_id)

conn = db_settings.con()
c = conn.cursor()
ad = 11
total_text = codecs.open(u"../../data/taipei/meeting_minutes-11.txt", "r", "utf-8").read()
util = json.load(open('../util.json'))

Session_Token = re.compile(u'''
    [\s]*
    (?P<name>
        (?P<county>[\W]{1,3}(市|縣))議會
        第(?P<ad>[\d]+)屆
        第(?P<session>[\d]+)次(?P<type>(定期|臨時))大會
        (預備會議暨)?
        第(?P<times>[\d]+)次
        會議
    )
    紀錄
''', re.X)

Present_Token = re.compile(u'''
    出席議員[:：]?
    (?P<names>.+?)
    (計[\d]+位)?
    (請假議員)?
    列席
''', re.X|re.S)

Absent_Token = re.compile(u'''
    請假議員[:：]
    (?P<names>.+)
    (計[\d]+位)?
    列席
''', re.X|re.S)

sittings = []
for match in Session_Token.finditer(total_text):
    if match:
        if match.group('type') == u'定期':
            uid = '%s-%02d-%02d-CS-%02d' % (util[match.group('county')], int(match.group('ad')), int(match.group('session')), int(match.group('times')))
        elif match.group('type') == u'臨時':
            uid = '%s-%02d-T%02d-CS-%02d' % (util[match.group('county')], int(match.group('ad')), int(match.group('session')), int(match.group('times')))
        sittings.append({"uid":uid, "name": match.group('name'), "county": match.group('county'), "date": common.GetDate(total_text), "start": match.start(), "end": match.end()})
for i in range(0, len(sittings)):
    print sittings[i]
    # --> sittings, attendance, filelog
    if i != len(sittings)-1:
        one_sitting_text = total_text[sittings[i]['start']:sittings[i+1]['start']]
    else:
        one_sitting_text = total_text[sittings[i]['start']:]
    common.InsertSitting(c, sittings[i])
    common.FileLog(c, sittings[i]['name'])
    present_match = Present_Token.search(one_sitting_text)
    if present_match:
        common.Attendance(c, sittings[i], present_match.group('names'), 'CS', 'present')
    absent_match = Absent_Token.search(one_sitting_text)
    if absent_match:
        common.Attendance(c, sittings[i], absent_match.group('names'), 'CS', 'absent')
    # <--
conn.commit()
