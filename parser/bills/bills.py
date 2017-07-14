#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
sys.path.append('../')
import json
import glob

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

def bill_party_diversity(bill_id):
    c.execute('''
        UPDATE bills_bills
        SET param = (COALESCE(param, '{}'::jsonb) || (
            select jsonb_build_object('diversity', (
                select jsonb_agg(row)
                    from (
                    select
                        c.party,
                        count(*) / (SUM(COUNT(*)) OVER()) as ratio
                    from bills_councilors_bills cb
                    join councilors_councilorsdetail c on c.id = cb.councilor_id
                    where cb.bill_id = %s
                    group by c.party
                    order by ratio desc
                ) row
            ))
        ))
        WHERE uid = %s
    ''', [bill_id, bill_id])

def personal_vector(councilor_id):
    c.execute('''
        UPDATE councilors_councilorsdetail
        SET param = (COALESCE(param, '{}'::jsonb) || (
            select jsonb_build_object('bills_party_diversity', (
                select jsonb_agg(row)
                from (
                    select
                        c.party,
                        count(*) / (SUM(COUNT(*)) OVER()) as ratio
                    from bills_councilors_bills cb
                    join councilors_councilorsdetail c on c.id = cb.councilor_id
                    where cb.bill_id in (
                        select bill_id
                        from bills_councilors_bills
                        where councilor_id = %s
                    )
                    group by c.party
                    order by ratio desc
                ) row
            ))
        ))
        where id = %s
    ''', [councilor_id, councilor_id])

def councilors(election_year, county):
    c.execute('''
        SELECT id
        FROM councilors_councilorsdetail
        WHERE election_year = %s AND county = %s
    ''', (election_year, county))
    return c.fetchall()

def update_sponsor_param(uid):
    c.execute('''
        update bills_bills
        set param = (COALESCE(param, '{}'::jsonb) || (
            select jsonb_build_object('sponsors_groupby_party', (
                select jsonb_object_agg("role", "detail")
                from (
                    select role, json_build_object('party_list', party_list, 'sum', sum) as detail
                    from (
    select role, json_agg(party_list) as party_list, sum(count)
                    from (
                    select role, json_build_object('party', party, 'councilors', councilors, 'count', json_array_length(councilors)) as party_list, json_array_length(councilors) as count
                    from (
                            select role, party, json_agg(detail) as councilors
                            from (
                                select role, party, json_build_object('name', name, 'councilor_id', councilor_id) as detail
                                from (
                                    select
                                        case
                                            WHEN priproposer = true AND petition = false THEN 'priproposer'
                                            WHEN petition = false THEN 'sponsor'
                                            WHEN petition = true THEN 'cosponsor'
                                        end as role,
                                        l.party,
                                        l.name,
                                        l.councilor_id
                                    from councilors_councilorsdetail l, bills_bills v , bills_councilors_bills vl
                                    where v.uid = %s and v.uid = vl.bill_id and vl.councilor_id = l.id
                                ) _
                            ) __
                            group by role, party
                            order by role, party
                        ) ___
                        order by role, count desc
                                        ) ____
                group by role
                order by sum desc
                ) _____
                ) row
            ))
        ))
        where uid = %s
	''', [uid, uid])

conn = db_settings.con()
c = conn.cursor()
election_year = common.election_year('')

for f in glob.glob('../../data/*/bills-%s.json' % election_year):
    county_abbr = f.split('/')[-2]
    county = common.county_abbr2string(county_abbr)
    county_abbr3 = common.county2abbr3(county)
    print f
    dict_list = json.load(open(f))
    for bill in dict_list:
        try:
            bill['county'] = county
            bill.update({'uid': u'%s-%s' % (bill['county'], bill['id'])})
            Bill(bill)
            priproposer = True
            for name in bill['proposed_by']:
                name = common.normalize_person_name(name)
                name = re.sub(u'副?議長', '', name)
                for councilor_id in common.GetCouncilorId(c, name):
                    id = common.getDetailIdFromUid(c, councilor_id, bill['election_year'], bill['county'])
                    if id:
                        CouncilorsBills(id, bill['uid'], priproposer, False)
                priproposer = False
            for name in bill.get('petitioned_by', []):
                name = re.sub(u'\(.*\)', '', name)
                name = re.sub(u'[˙・•．]', u'‧', name)
                name = name.strip()
                name = re.sub(u'副?議長', '', name)
                for councilor_id in common.GetCouncilorId(c, name):
                    id = common.getDetailIdFromUid(c, councilor_id, bill['election_year'], bill['county'])
                    if id:
                        CouncilorsBills(id, bill['uid'], False, True)
            update_sponsor_param(bill['uid'])
            bill_party_diversity(bill['uid'])
        except Exception, e:
            print bill
            print e
    # Update bills_party_diversity of People
    for councilor_id in councilors(election_year, county):
        personal_vector(councilor_id)
conn.commit()
print 'bills done'

c.execute('''
    SELECT
        councilor_id,
        COUNT(*) total,
        SUM(CASE WHEN priproposer = true AND petition = false THEN 1 ELSE 0 END) priproposer,
        SUM(CASE WHEN petition = false THEN 1 ELSE 0 END) sponsor,
        SUM(CASE WHEN petition = true THEN 1 ELSE 0 END) cosponsor
    FROM bills_councilors_bills
    GROUP BY councilor_id
''')
response = c.fetchall()
for r in response:
    param = dict(zip(['total', 'priproposer', 'sponsor', 'cosponsor'], r[1:]))
    c.execute('''
        UPDATE councilors_councilorsdetail
        SET param = (COALESCE(param, '{}'::jsonb) || %s::jsonb)
        WHERE id = %s
    ''', (json.dumps({'bills_role_statistics': param}), r[0]))
conn.commit()
print 'Update bills_role_statistics of People done'
