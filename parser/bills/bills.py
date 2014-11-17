#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
sys.path.append('../')
import psycopg2
import json
import db_settings
import common


def Bill(bill):
    complement = {'type': '', 'category': '', 'abstract': '', 'description': '', 'methods': '', 'last_action': '', 'proposed_by': '', 'petitioned_by': '', 'bill_no': '', 'brought_by': '', 'related_units': '', 'committee': '', 'motions': None, 'execution': '', 'remark': '', 'links': ''}
    complement.update(bill)
    complement['proposed_by'] = ' '.join(complement['proposed_by'])
    complement['petitioned_by'] = ' '.join(complement['petitioned_by'])
    c.execute('''
        UPDATE bills_bills
        SET election_year = %(election_year)s, county = %(county)s, type = %(type)s, category = %(category)s, abstract = %(abstract)s, description = %(description)s, methods = %(methods)s, last_action = %(last_action)s, proposed_by = %(proposed_by)s, petitioned_by = %(petitioned_by)s, brought_by = %(brought_by)s, related_units = %(related_units)s, committee = %(committee)s, motions = %(motions)s, execution = %(execution)s, bill_no = %(bill_no)s, remark = %(remark)s, links = %(links)s
        WHERE uid = %(uid)s
    ''', complement)
    c.execute('''
        INSERT into bills_bills(uid, election_year, county, type, category, abstract, description, methods, last_action, proposed_by, petitioned_by, brought_by, related_units, committee, bill_no, motions, execution, remark, links)
        SELECT %(uid)s, %(election_year)s, %(county)s, %(type)s, %(category)s, %(abstract)s, %(description)s, %(methods)s, %(last_action)s, %(proposed_by)s, %(petitioned_by)s, %(brought_by)s, %(related_units)s, %(committee)s, %(bill_no)s, %(motions)s, %(execution)s, %(remark)s, %(links)s
        WHERE NOT EXISTS (SELECT 1 FROM bills_bills WHERE uid = %(uid)s)
    ''', complement)

def CouncilorsBills(councilor_id, bill_id, priproposer, petition):
    c.execute('''
        INSERT into bills_councilors_bills(councilor_id, bill_id, priproposer, petition)
        SELECT %s, %s, %s, %s
        WHERE NOT EXISTS (SELECT 1 FROM bills_councilors_bills WHERE councilor_id = %s AND bill_id = %s)
    ''', (councilor_id, bill_id, priproposer, petition, councilor_id, bill_id))

conn = db_settings.con()
c = conn.cursor()

for council in ['../../data/chcc/bills.json', '../../data/cyscc/bills.json', '../../data/ntcc/bills.json', '../../data/hlcc/bills.json', '../../data/tncc/bills.json', '../../data/ntp/bills.json', '../../data/kcc/bills.json', '../../data/tccc/bills.json', '../../data/tcc/bills.json']:
    print council
    dict_list = json.load(open(council))
    for bill in dict_list:
        print bill
        bill.update({'uid': u'%s-%s' % (bill['county'], bill['id'])})
        Bill(bill)
        priproposer = True
        for name in bill['proposed_by']:
            name = re.sub(u'\(.*\)', '', name)
            name = re.sub(u'[˙・•．]', u'‧', name)
            name = name.strip()
            if name == u'笛布斯‧顗賚':
                name = u'笛布斯顗賚'
            name = re.sub(u'副?議長', '', name)
            councilor_id = common.getDetailId(c, name, bill['election_year'], bill['county'])
            if councilor_id:
                CouncilorsBills(councilor_id, bill['uid'], priproposer, False)
            priproposer = False
        for name in bill.get('petitioned_by', []):
            name = re.sub(u'\(.*\)', '', name)
            name = re.sub(u'[˙・•．]', u'‧', name)
            name = name.strip()
            if name == u'笛布斯‧顗賚':
                name = u'笛布斯顗賚'
            councilor_id = common.getDetailId(c, name, bill['election_year'], bill['county'])
            if councilor_id:
                CouncilorsBills(councilor_id, bill['uid'], False, True)
    conn.commit()
print 'bills done'

def bill_party_diversity(parties):
    c.execute('''
        select
            b.bill_id,
            count(*) total,
            %s
        from councilors_councilorsdetail a, bills_councilors_bills b
        where a.id = b.councilor_id
        group by b.bill_id
    ''' % ', '.join(["sum(case when a.party = '%s' then 1 else 0 end)" % x for x in parties]))
    for bill in c.fetchall():
        bill = list(bill)
        percentage = [x/float(bill[1]) for x in bill[2:]]
        c.execute('''
            UPDATE bills_bills
            SET param = %s
            WHERE uid = %s
        ''', ({'diversity': dict(zip(parties, percentage))}, bill[0]))

def personal_vector(parties, councilor_id):
    c.execute('''
        SELECT a.param::json->'diversity'
        FROM bills_bills a, bills_councilors_bills b
        WHERE a.uid = b.bill_id AND b.councilor_id = %s
    ''', (councilor_id, ))
    r = c.fetchall()
    diversity = {}
    for party in parties:
        if r:
            diversity.update({party: sum([x[0][party.decode('utf8')] for x in r]) / float(len(r))})
    c.execute('''
        UPDATE councilors_councilorsdetail
        SET param = %s
        WHERE id = %s
    ''', ({'diversity': diversity}, councilor_id))

def councilors(election_year, county):
    c.execute('''
        SELECT id
        FROM councilors_councilorsdetail
        WHERE election_year = %s AND county = %s
    ''', (election_year, county))
    return c.fetchall()

def distinct_party(election_year, county):
    c.execute('''
        SELECT DISTINCT(party)
        FROM councilors_councilorsdetail
        WHERE election_year = %s AND county = %s
        ORDER BY party
    ''', (election_year, county))
    return c.fetchall()

for election_year, county in [('2010', u'臺北市'), ('2010', u'臺中市'), ('2010', u'高雄市'), ('2010', u'新北市')]:
    parties = [x[0] for x in distinct_party(election_year, county)]
    bill_party_diversity(parties)
    for councilor_id in councilors(election_year, county):
        personal_vector(parties, councilor_id)
    conn.commit()
print 'bills diversity done'
