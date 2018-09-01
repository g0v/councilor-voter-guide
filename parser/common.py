# -*- coding: utf-8 -*-
import re
import uuid
import codecs
import psycopg2
import json
from datetime import datetime
import logging


logging.basicConfig(filename='common.log', level=logging.INFO)

def storage_domain():
    return 'https://drsgjxdg6zyfq.cloudfront.net'

def last_election_years(election_year):
    return {
        '2018': ['2014'],
        '2014': ['2010', '2009'],
        '2010': ['2006'],
        '2009': ['2005'],
        '2006': ['2002'],
        '2005': ['2001'],
        '2002': ['1998'],
        '2001': ['1997']
    }[election_year]

def election_year(county):
    return '2014'

def get_elected_legislator_candidate_info(c, candidate):
    c.execute('''
        select row_to_json(_)
        from (
            SELECT c.birth, ct.politicalcontributions, ct.cec_data, ct.county, ct.constituency
            FROM candidates_candidates c, candidates_terms ct, legislator_legislatordetail ld
            WHERE c.uid = ct.candidate_id AND ld.id = ct.legislator_id AND ld.legislator_id = %s
            ORDER BY ct.ad DESC
        ) _
    ''', [candidate['legislator_uid'], ])
    r = c.fetchone()
    if r:
        return r[0]

def get_legislator_candidate_info(c, name):
    identifiers = {name, re.sub(u'[\w‧]', '', name), re.sub(u'\W', '', name).lower(), } - {''}
    if identifiers:
        c.execute('''
            SELECT uid
            FROM candidates_candidates
            WHERE identifiers ?| array[%s]
        ''' % ','.join(["'%s'" % x for x in identifiers]))
        r = c.fetchone()
        if r:
            candidate_uid = r[0]
            c.execute('''
                SELECT row_to_json(_)
                FROM (
                    SELECT c.birth, ct.politicalcontributions, ct.cec_data, ct.county, ct.constituency
                    FROM candidates_candidates c, candidates_terms ct
                    WHERE c.uid = ct.candidate_id AND ct.candidate_id = %s
                    ORDER BY ad DESC
                ) _
            ''', [candidate_uid, ])
            r = c.fetchone()
            if r:
                return r[0]

def get_legislator_data(c, uid):
    c.execute('''
        SELECT data
        FROM legislator_legislator
        WHERE uid = %s
    ''', [uid])
    return c.fetchone()

def get_legislator_uid(c, name):
    identifiers = {name, re.sub(u'[\w‧]', '', name), re.sub(u'\W', '', name).lower(), } - {''}
    if identifiers:
        c.execute('''
            SELECT uid
            FROM legislator_legislator
            WHERE identifiers ?| array[%s]
        ''' % ','.join(["'%s'" % x for x in identifiers]))
        return c.fetchone()

def get_legislator_standpoints(c, term):
    c.execute(u'''
        SELECT json_agg(row)
        FROM (
            SELECT
            CASE
                WHEN lv.decision = 1 THEN '贊成'
                WHEN lv.decision = -1 THEN '反對'
                WHEN lv.decision = 0 THEN '棄權'
                WHEN lv.decision isnull THEN '沒投票'
            END as decision,
            s.title,
            count(*) as times
        FROM vote_legislator_vote lv
        JOIN legislator_legislatordetail ld on ld.id = lv.legislator_id
        JOIN standpoint_standpoint s on s.vote_id = lv.vote_id
        WHERE ld.legislator_id = %s AND s.pro = (
            SELECT max(pro)
            FROM standpoint_standpoint ss
            WHERE ss.pro > 0 AND s.vote_id = ss.vote_id
            GROUP BY ss.vote_id
        )
        GROUP BY s.title, lv.decision
        ORDER BY times DESC
        LIMIT 5
        ) row
    ''', [term['legislator_id'], ])
    r = c.fetchone()
    return r[0] if r else []

def legislator_terms(c, candidate):
    ref = {'2022': 10, '2018': 9, '2014': 8, '2010': 7, '2009': 7}
    candidate['ad'] = ref[candidate['election_year']]
    c.execute('''
        SELECT l.id as term_id, l.legislator_id, l.ad, l.county, l.bill_param, l.vote_param, l.attendance_param, to_char(EXTRACT(YEAR FROM l.term_start), '9999') as term_start_year, substring(l.term_end->>'date' from '(\d+)-') as term_end_year, COALESCE(c.cec_data->>'rptpolitics', l.platform, c.platform) as platform, in_office, term_end
        FROM legislator_legislatordetail l
        LEFT JOIN candidates_terms c ON c.legislator_id = l.id
        WHERE l.legislator_id = %(legislator_uid)s AND l.ad <= %(ad)s
        ORDER BY l.ad DESC
    ''', candidate)
    key = [desc[0] for desc in c.description]
    terms = []
    r = c.fetchall()
    for row in r:
        data = dict(zip(key, row))
        data['standpoints'] = get_legislator_standpoints(c, data)
        terms.append(data)
    return terms

def get_mayor_standpoints(c, term):
    c.execute(u'''
        SELECT json_agg(row)
        FROM (
            SELECT
                s.title,
                count(*) as times,
                sum(pro) as pro
            FROM bills_mayors_bills lv
            JOIN standpoints_standpoints s on s.bill_id = lv.bill_id
            JOIN mayors_terms mt on mt.uid = lv.mayor_id
            WHERE mt.mayor_id = %s AND s.pro = (
                SELECT max(pro)
                FROM standpoints_standpoints ss
                WHERE ss.pro > 0 AND s.bill_id = ss.bill_id
                GROUP BY ss.bill_id
            )
            GROUP BY s.title
            ORDER BY pro DESC, times DESC
            LIMIT 5
        ) row
    ''', [term['mayor_id'], ])
    r = c.fetchone()
    return r[0] if r else []

def mayor_terms(c, candidate):
    c.execute('''
        SELECT uid as term_id, mayor_id, election_year, county, data, to_char(EXTRACT(YEAR FROM term_start), '9999') as term_start_year, substring(term_end->>'date' from '(\d+)-') as term_end_year, platform, in_office, term_end
        FROM mayors_terms
        WHERE mayor_id = %(mayor_uid)s AND election_year <= %(election_year)s
        ORDER BY election_year DESC
    ''', candidate)
    key = [desc[0] for desc in c.description]
    terms = []
    r = c.fetchall()
    for row in r:
        data = dict(zip(key, row))
        data['standpoints'] = get_mayor_standpoints(c, data)
        terms.append(data)
    return terms

def councilor_terms(c, candidate):
    '''
    Parse working recoed before the election_year of this candidate into a json to store in individual candidate, so we could display councilor's working records easier at candidate page(no need of a lot of reference).
    '''

    c.execute('''
        SELECT cd.id as term_id, cd.councilor_id, cd.election_year, cd.county, cd.constituency, cd.param, to_char(EXTRACT(YEAR FROM cd.term_start), '9999') as term_start_year, substring(cd.term_end->>'date' from '(\d+)-') as term_end_year, cd.platform, cd.in_office, cd.term_end, ct.votes, ct.votes_percentage, ct.votes_detail, ct.party as elected_party
        FROM councilors_councilorsdetail cd
        LEFT JOIN candidates_terms ct ON ct.elected_councilor_id = cd.id
        WHERE cd.councilor_id = %(councilor_uid)s AND cd.election_year <= %(election_year)s
        ORDER BY cd.election_year DESC
    ''', candidate)
    key = [desc[0] for desc in c.description]
    terms = []
    r = c.fetchall()
    for row in r:
        terms.append(dict(zip(key, row)))
    return terms

def get_or_create_councilor_uid(c, councilor, create=True):
    '''
        return councilor_uid, created
    '''
    logging.info(councilor)
    councilor['councilor_ids'] = tuple(GetCouncilorId(c, councilor['name']))
    if not councilor['councilor_ids']:
        if create:
            return (str(uuid.uuid4()), False)
        else:
            return (None, False)
    counties = {
        u'新北市': [u'新北市', u'臺北縣'],
        u'臺北縣': [u'新北市', u'臺北縣'],
        u'桃園市': [u'桃園市', u'桃園縣'],
        u'桃園縣': [u'桃園市', u'桃園縣'],
        u'臺中市': [u'臺中市', u'臺中縣'],
        u'臺中縣': [u'臺中市', u'臺中縣'],
        u'臺南市': [u'臺南市', u'臺南縣'],
        u'臺南縣': [u'臺南市', u'臺南縣'],
        u'高雄市': [u'高雄市', u'高雄縣'],
        u'高雄縣': [u'高雄市', u'高雄縣']
    }
    councilor['counties'] = tuple(counties.get(councilor['county'], [councilor['county']]))
    c.execute('''
        SELECT councilor_id
        FROM councilors_councilorsdetail
        WHERE councilor_id in %(councilor_ids)s AND county in %(counties)s
        ORDER BY
            CASE
                WHEN election_year = %(election_year)s AND constituency = %(constituency)s AND name = %(name)s THEN 1
                WHEN election_year = %(election_year)s AND constituency = %(constituency)s THEN 2
                WHEN constituency = %(constituency)s AND name = %(name)s THEN 3
                WHEN constituency = %(constituency)s THEN 4
                WHEN name = %(name)s THEN 5
            END,
            election_year DESC
        LIMIT 1
    ''', councilor)
    r = c.fetchone()
    if r:
        return (r[0], True)
    elif create:
        return (str(uuid.uuid4()), False)
    print councilor['name']
    return (None, False)

def get_or_create_moyor_candidate_uid(c, candidate, create=True):
    '''
        return candidate_uid, created
    '''
    logging.info(candidate)
    candidate['candidate_ids'] = tuple(GetPossibleCandidateIds(c, candidate['name']))
    if not candidate['candidate_ids']:
        if create:
            return (str(uuid.uuid4()), False)
        else:
            return (None, False)
    c.execute('''
        SELECT candidate_id
        FROM candidates_terms
        WHERE candidate_id in %(candidate_ids)s
        ORDER BY
            CASE
                WHEN election_year = %(election_year)s AND constituency = %(constituency)s AND name = %(name)s THEN 1
                WHEN election_year = %(election_year)s AND constituency = %(constituency)s THEN 2
                WHEN constituency = %(constituency)s AND name = %(name)s THEN 3
                WHEN constituency = %(constituency)s THEN 4
                WHEN name = %(name)s THEN 5
            END,
            election_year DESC
        LIMIT 1
    ''', candidate)
    r = c.fetchone()
    if r:
        return (r[0], True)
    elif create:
        return (str(uuid.uuid4()), False)
    print candidate['name']
    return (None, False)

def is_mayor_occupy(c, candidate):
    c.execute('''
        SELECT 1
        FROM mayors_terms
        WHERE mayor_id = %s AND in_office = true AND election_year in %s
    ''', [candidate['mayor_uid'], tuple(last_election_years(candidate['election_year']))])
    r = c.fetchone()
    if r:
        return True

def mayor_image(c, candidate):
    c.execute('''
        SELECT image
        FROM mayors_terms
        WHERE mayor_id = %s AND in_office = true AND election_year in %s
    ''', [candidate['mayor_uid'], tuple(last_election_years(candidate['election_year']))])
    r = c.fetchone()
    if r:
        return r[0]

def is_councilor_occupy(c, candidate):
    c.execute('''
        SELECT 1
        FROM councilors_councilorsdetail
        WHERE councilor_id = %s AND in_office = true AND election_year in %s
    ''', [candidate['councilor_uid'], tuple(last_election_years(candidate['election_year']))])
    r = c.fetchone()
    if r:
        return True

def councilor_image(c, candidate):
    c.execute('''
        SELECT image
        FROM councilors_councilorsdetail
        WHERE councilor_id = %s AND in_office = true AND election_year in %s
    ''', [candidate['councilor_uid'], tuple(last_election_years(candidate['election_year']))])
    r = c.fetchone()
    if r:
        return r[0]

def get_or_create_candidate_uid(c, candidate, create=True):
    '''
        return candidate_uid, created
    '''
    logging.info(candidate)
    candidate['candidate_ids'] = tuple(GetPossibleCandidateIds(c, candidate['name']))
    if not candidate['candidate_ids']:
        if create:
            return (str(uuid.uuid4()), False)
        else:
            return (None, False)
    counties = {
        u'新北市': [u'新北市', u'臺北縣'],
        u'臺北縣': [u'新北市', u'臺北縣'],
        u'桃園市': [u'桃園市', u'桃園縣'],
        u'桃園縣': [u'桃園市', u'桃園縣'],
        u'臺中市': [u'臺中市', u'臺中縣'],
        u'臺中縣': [u'臺中市', u'臺中縣'],
        u'臺南市': [u'臺南市', u'臺南縣'],
        u'臺南縣': [u'臺南市', u'臺南縣'],
        u'高雄市': [u'高雄市', u'高雄縣'],
        u'高雄縣': [u'高雄市', u'高雄縣']
    }
    candidate['counties'] = tuple(counties.get(candidate['county'], [candidate['county']]))
    c.execute('''
        SELECT candidate_id
        FROM candidates_terms
        WHERE candidate_id in %(candidate_ids)s AND county in %(counties)s
        ORDER BY
            CASE
                WHEN election_year = %(election_year)s AND constituency = %(constituency)s AND name = %(name)s THEN 1
                WHEN election_year = %(election_year)s AND constituency = %(constituency)s THEN 2
                WHEN constituency = %(constituency)s AND name = %(name)s THEN 3
                WHEN constituency = %(constituency)s THEN 4
                WHEN name = %(name)s THEN 5
            END,
            election_year DESC
        LIMIT 1
    ''', candidate)
    r = c.fetchone()
    if r:
        return (r[0], True)
    elif create:
        return (str(uuid.uuid4()), False)
    print candidate['name']
    return (None, False)

def make_variants_set(string):
    variants = set([string])
    for variant in [(u'麗', u'麗'), (u'林', u'林'), (u'李', u'李'), (u'玲', u'玲'), (u'勳', u'勲'), (u'溫', u'温'), (u'黃', u'黄'), (u'寶', u'寳'), (u'真', u'眞'), (u'福', u'褔'), (u'鎮', u'鎭'), (u'妍', u'姸'), (u'市', u'巿'), (u'衛', u'衞'), (u'館', u'舘'), (u'峰', u'峯'), (u'群', u'羣'), (u'啟', u'啓'), (u'鳳', u'鳯'), (u'冗', u'宂'), (u'穀', u'榖'), (u'曾', u'曽'), (u'賴', u'頼'), (u'蒓', u'莼'), (u'靜', u'静'), (u'崐', u'崑'), (u'劉', u'劉'), ]:
        for item in variants.copy():
            variants.add(re.sub(variant[0], variant[1], item))
            variants.add(re.sub(variant[1], variant[0], item))
    return variants

def normalize_person_name(name):
    name_bk = name
    name = re.sub(u'(.+?\w+) (\w+)', u'\g<1>‧\g<2>', name) # e.g. Cemelesai Ljaljegan=>Cemelesai‧jaljegan
    if name != name_bk:
        print name
    name = re.sub(u'[。˙・･•．.-]', u'‧', name)
    name = re.sub(u'[　\s()（）’\'^]', '',name)
    name = name.title()
    return name

def normalize_party(party):
    party = party.strip()
    party = re.sub(u'籍$', '', party)
    party = re.sub(u'無政?黨?$', u'無黨籍', party)
    party = re.sub(u'^無黨籍及未經政黨推薦$', u'無黨籍', party)
    party = re.sub(u'台灣', u'臺灣', party)
    party = re.sub(u'台聯黨', u'臺灣團結聯盟', party)
    party = re.sub(u'社民黨', u'社會民主黨', party)
    party = re.sub(u'^國民黨$', u'中國國民黨', party)
    party = re.sub(u'^民進黨$', u'民主進步黨', party)
    return party

def SittingsAbbreviation(key):
    d = json.load(open('util.json'))
    return d.get(key)

def FileLog(c, sitting):
    c.execute('''
        INSERT into councilors_filelog(sitting, date)
        SELECT %s, %s
        WHERE NOT EXISTS (SELECT 1 FROM councilors_filelog WHERE sitting = %s) RETURNING id
    ''', (sitting, datetime.now(), sitting))

def ROC2AD(text):
    matchTerm = re.search(u'''
        (?P<year>[\d]+)[\s]*(?:年|[-/.])[\s]*
        (?P<month>[\d]+)[\s]*(?:月|[-/.])[\s]*
        (?P<day>[\d]+)
    ''', text, re.X)
    if matchTerm:
        return '%04d-%02d-%02d' % (int(matchTerm.group('year'))+1911, int(matchTerm.group('month')), int(matchTerm.group('day')))

def getId(c, name, election_year, county):
    c.execute('''
        SELECT councilor_id
        FROM councilors_councilorsdetail
        WHERE name = %s and election_year = %s and county = %s
    ''', (name, election_year, county))
    r = c.fetchone()
    if r:
        return r[0]
    print '"%s"' % name

def getDetailIdFuzzy(c, name, election_year, county):
    m = re.match(u'(?P<cht>.+?)[a-zA-Z]', name)
    if m:
        name = m.group('cht')
    c.execute('''
        SELECT id
        FROM councilors_councilorsdetail
        WHERE name like %s and election_year = %s and county = %s
    ''', (name + '%', election_year, county))
    r = c.fetchone()
    if r:
        return r[0]
    print '"%s"' % name

def getDetailIdFromUid(c, uid, election_year, county):
    c.execute('''
        SELECT id
        FROM councilors_councilorsdetail
        WHERE councilor_id = %s and election_year = %s and county = %s
    ''', (str(uid), election_year, county))
    r = c.fetchone()
    if r:
        return r[0]

def getDetailId(c, name, election_year, county):
    c.execute('''
        SELECT id
        FROM councilors_councilorsdetail
        WHERE name = %s and election_year = %s and county = %s
    ''', (name, election_year, county))
    r = c.fetchone()
    if r:
        return r[0]
    else:
        return getDetailIdFuzzy(c, name, election_year, county)

def getIdList(c, name_list, sitting_dict):
    c.execute('''
        SELECT id, councilor_id
        FROM councilors_councilorsdetail
        WHERE name IN %s and election_year = %s and county = %s
    ''', (tuple(name_list), sitting_dict['election_year'], sitting_dict['county']))
    r = c.fetchall()
    if r:
        return r
    for name in name_list:
        print '"%s"' % name
    #raw_input()
    return []

def GetPossibleCandidateIds(c, name):
    identifiers = {name, re.sub(u'[\w。˙・･•．.‧’\']', '', name), re.sub(u'\W', '', name).lower(), } - {''}
    if identifiers:
        c.execute('''
            SELECT uid
            FROM candidates_candidates
            WHERE identifiers ?| array[%s]
        ''' % ','.join(["'%s'" % x for x in identifiers]))
        return [x[0] for x in c.fetchall()]

def GetCouncilorId(c, name):
    identifiers = {name, re.sub(u'[\w。˙・･•．.‧’〃\']', '', name), re.sub(u'\W', '', name).lower(), } - {''}
    if identifiers:
        c.execute('''
            SELECT uid
            FROM councilors_councilors
            WHERE identifiers ?| array[%s]
        ''' % ','.join(["'%s'" % x for x in identifiers]))
        r = c.fetchall()
        if r:
            return [x[0] for x in r]
        else:
            logging.error(u'%s not an councilor?' % name)
    return []

def getCouncilorIdList(c, text):
    id_list = []
    text = text.strip(u'[　\s]')
    text = re.sub(u'[　\n]', u' ', text)
    text = re.sub(u'[ ]+(\d+)[ ]+', u'\g<1>', text)
    text = re.sub(u' ([^ \w]) ([^ \w]) ', u' \g<1>\g<2> ', text) # e.g. 楊　曜=>楊曜, 包含句首
    text = re.sub(u'^([^ \w]) ([^ \w]) ', u'\g<1>\g<2> ', text) # e.g. 楊　曜=>楊曜, 包含句首
    text = re.sub(u' ([^ \w]) ([^ \w])$', u' \g<1>\g<2>', text) # e.g. 楊　曜=>楊曜, 包含句尾
    text = re.sub(u' (\w+) (\w+) ', u' \g<1>\g<2> ', text) # e.g. Kolas Yotaka=>KolasYotaka, 包含句首
    text = re.sub(u'^(\w+) (\w+) ', u'\g<1>\g<2> ', text) # e.g. Kolas Yotaka=>KolasYotaka, 包含句首
    text = re.sub(u'　(\w+) (\w+)$', u' \g<1>\g<2>', text) # e.g. Kolas Yotaka=>KolasYotaka, 包含句尾
    text = re.sub(u'^([^ \w]) ([^ \w])$', u'\g<1>\g<2>', text) # e.g. 楊　曜=>楊曜, 單獨一人
    text = re.sub(u'^(\w+) (\w+)$', u'\g<1>\g<2>', text) # e.g. Kolas Yotaka=>KolasYotaka, 單獨一人
    for name in text.split():
        name = re.sub(u'(.*)[）)。】」]$', '\g<1>', name) # 名字後有標點符號
        councilor_ids = GetCouncilorId(c, name)
        if councilor_ids:
            id_list.extend(councilor_ids)
        else:
            logging.error(u'%s not an councilor?' % name)
    return id_list

def AddAttendanceRecord(c, councilor_id, sitting_id, category, status):
    c.execute('''
        INSERT into councilors_attendance(councilor_id, sitting_id, category, status)
        SELECT %s, %s, %s, %s
        WHERE NOT EXISTS (SELECT 1 FROM councilors_attendance WHERE councilor_id = %s AND sitting_id = %s)
    ''', (councilor_id, sitting_id, category, status, councilor_id, sitting_id))

def Attendance(c, sitting_dict, text, category, status):
    ids = []
    for councilor_id in getCouncilorIdList(c, text):
        id = getDetailIdFromUid(c, councilor_id, sitting_dict['election_year'], sitting_dict['county'])
        if id:
            AddAttendanceRecord(c, id, sitting_dict['uid'], category, status)
            ids.append(id)
        else:
            logging.error(u'uid:%s not exist terms of %s, %s' % (councilor_id, sitting_dict['election_year'], sitting_dict['county']))
    return ids

def InsertSitting(c, sitting_dict):
    complement = {"committee": '', "name": ''}
    complement.update(sitting_dict)
    c.execute('''
        UPDATE sittings_sittings
        SET name = %(name)s, election_year = %(election_year)s, date = %(date)s, county = %(county)s, committee = %(committee)s
        WHERE uid = %(uid)s
    ''', complement)
    c.execute('''
        INSERT into sittings_sittings(uid, name, election_year, date, county, committee)
        SELECT %(uid)s, %(name)s, %(election_year)s, %(date)s, %(county)s, %(committee)s
        WHERE NOT EXISTS (SELECT 1 FROM sittings_sittings WHERE uid = %(uid)s)
    ''', complement)

def UpdateSittingLinks(c, meeting):
    c.execute('''
        UPDATE sittings_sittings
        SET links = %(links)s
        WHERE name = %(name)s
        RETURNING id
    ''', meeting)
    if not c.fetchall():
        c.execute('''
            UPDATE sittings_sittings
            SET links = %(links)s
            WHERE county = %(county)s AND date = %(date)s
        ''', meeting)

def county_abbr2string(abbr):
    return {
        'ntp': u'新北市',
        'tcc': u'臺北市',
        'tycc': u'桃園市',
        'kmc': u'基隆市',
        'ilcc': u'宜蘭縣',
        'hcc': u'新竹縣',
        'hsinchucc': u'新竹市',
        'mcc': u'苗栗縣',
        'tccc': u'臺中市',
        'chcc': u'彰化縣',
        'ylcc': u'雲林縣',
        'ntcc': u'南投縣',
        'cyscc': u'嘉義縣',
        'cycc': u'嘉義市',
        'tncc': u'臺南市',
        'kcc': u'高雄市',
        'ptcc': u'屏東縣',
        'hlcc': u'花蓮縣',
        'taitungcc': u'臺東縣',
        'mtcc': u'連江縣',
        'kmcc': u'金門縣',
        'phcouncil': u'澎湖縣'
    }[abbr]

def county2abbr3(county):
    return {
        u"新北市": "TPQ",
        u"臺北市": "TPE",
        u"臺中市": "TXG",
        u"臺南市": "TNN",
        u"高雄市": "KHH",
        u"基隆市": "KEE",
        u"新竹市": "HSZ",
        u"嘉義市": "CYI",
        u"桃園縣": "TAO",
        u"桃園市": "TAO",
        u"新竹縣": "HSQ",
        u"苗栗縣": "MIA",
        u"彰化縣": "CHA",
        u"南投縣": "NAN",
        u"雲林縣": "YUN",
        u"嘉義縣": "CYQ",
        u"屏東縣": "PIF",
        u"宜蘭縣": "ILA",
        u"花蓮縣": "HUA",
        u"臺東縣": "TTT",
        u"澎湖縣": "PEN",
        u"高雄縣": "KHQ",
        u"臺南縣": "TNQ",
        u"臺北縣": "TPQ",
        u"臺中縣": "TXQ",
        u"金門縣": "JME",
        u"連江縣": "LJF"
    }[county]

def normalize_constituency(constituency):
    try:
        return int(constituency)
    except:
        pass
    match = re.search(u'第(?P<num>.+)選(?:舉)?區', constituency)
    if not match:
        return None
    try:
        return int(match.group('num'))
    except:
        logging.info(match.group('num'))
    ref = {u'一': 1, u'二': 2, u'三': 3, u'四': 4, u'五': 5, u'六': 6, u'七': 7, u'八': 8, u'九': 9}
    if re.search(u'^\s*十\s*$', match.group('num')):
        return 10
    num = re.sub(u'^\s*十', u'一', match.group('num'))
    num = re.sub(u'十', '', num)
    digits = re.findall(u'(一|二|三|四|五|六|七|八|九)', num)
    total, dec = 0, 1
    for i in reversed(range(0, len(digits))):
        total = total + int(ref.get(digits[i], 0)) * dec
        dec = dec * 10
    return total

def get_term_range(county, election_year):
    return {
        "臺北市": {'1969': 1, '1973': 2, '1977': 3, '1981': ['1981-12-25', '1985-12-25'], '1985': ['1985-12-25', '1989-12-25'], '1989': ['1989-12-25', '1994-12-25'], '1994': ['1994-12-25', '1998-12-25'], '1998': ['1998-12-25', '2002-12-25'], '2002': ['2002-12-25', '2006-12-25'], '2006': ['2006-12-25', '2010-12-25'], '2010': ['2010-12-25', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "高雄市": {'1981': ['1981-12-25', '1985-12-25'], '1985': ['1985-12-25', '1989-12-25'], '1989': ['1989-12-25', '1994-12-25'], '1994': ['1994-12-25', '1998-12-25'], '1998': ['1998-12-25', '2002-12-25'], '2002': ['2002-12-25', '2006-12-25'], '2006': ['2006-12-25', '2010-12-25'], '2010': ['2010-12-25', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "高雄縣": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-12-25']},
        "新北市": {'2010': ['2010-12-25', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "臺北縣": {'1951': 1, '1953': 2, '1955': 3, '1958': 4, '1961': 5, '1964': 6, '1968': 7, '1973': 8, '1977': 9, '1982': 10, '1986': 11, '1990': 12, '1994': 13, '1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-12-25']},
        "臺南市": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-12-25'], '2010': ['2010-12-25', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "臺南縣": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-12-25']},
        "臺中市": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-12-25'], '2010': ['2010-12-25', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "臺中縣": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-12-25']},
        "桃園市": {'2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "桃園縣": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-02-28'], '2009': ['2010-03-01', '2014-12-25']},
        "南投縣": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-02-28'], '2009': ['2010-03-01', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "宜蘭縣": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-02-28'], '2009': ['2010-03-01', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "澎湖縣": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-02-28'], '2009': ['2010-03-01', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "屏東縣": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-02-28'], '2009': ['2010-03-01', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "新竹市": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-02-28'], '2009': ['2010-03-01', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "新竹縣": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-02-28'], '2009': ['2010-03-01', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "雲林縣": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-02-28'], '2009': ['2010-03-01', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "基隆市": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-02-28'], '2009': ['2010-03-01', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "嘉義縣": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-02-28'], '2009': ['2010-03-01', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "彰化縣": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-02-28'], '2009': ['2010-03-01', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "臺東縣": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-02-28'], '2009': ['2010-03-01', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "花蓮縣": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-02-28'], '2009': ['2010-03-01', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "嘉義市": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-02-28'], '2009': ['2010-03-01', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "苗栗縣": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-02-28'], '2009': ['2010-03-01', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "連江縣": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-02-28'], '2009': ['2010-03-01', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
        "金門縣": {'1998': ['1998-03-01', '2002-02-28'], '2002': ['2002-03-01', '2006-02-28'], '2005': ['2006-03-01', '2010-02-28'], '2009': ['2010-03-01', '2014-12-25'], '2014': ['2014-12-25', '2018-12-25'], '2018': ['2018-12-25', '2022-12-25']},
    }[county].get(election_year)

