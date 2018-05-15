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
    complement = {'type': '', 'category': '', 'abstract': '', 'description': '', 'methods': '', 'last_action': '', 'proposed_by': '', 'petitioned_by': '', 'bill_no': '', 'brought_by': '', 'related_units': '', 'committee': '', 'motions': None, 'execution': '', 'remark': '', 'link': '', 'links': None}
    complement.update(bill)
    complement['proposed_by'] = ' '.join(complement['proposed_by'])
    complement['petitioned_by'] = ' '.join(complement['petitioned_by'])
    c.execute('''
        INSERT INTO bills_bills(uid, election_year, county, type, category, abstract, description, methods, last_action, proposed_by, petitioned_by, brought_by, related_units, committee, bill_no, motions, execution, remark, link, links)
        VALUES (%(uid)s, %(election_year)s, %(county)s, %(type)s, %(category)s, %(abstract)s, %(description)s, %(methods)s, %(last_action)s, %(proposed_by)s, %(petitioned_by)s, %(brought_by)s, %(related_units)s, %(committee)s, %(bill_no)s, %(motions)s, %(execution)s, %(remark)s, %(link)s, %(links)s)
        ON CONFLICT (uid)
        DO UPDATE
        SET election_year = %(election_year)s, county = %(county)s, type = %(type)s, category = %(category)s, abstract = %(abstract)s, description = %(description)s, methods = %(methods)s, last_action = %(last_action)s, proposed_by = %(proposed_by)s, petitioned_by = %(petitioned_by)s, brought_by = %(brought_by)s, related_units = %(related_units)s, committee = %(committee)s, motions = %(motions)s, execution = %(execution)s, bill_no = %(bill_no)s, remark = %(remark)s, link = %(link)s, links = %(links)s
    ''', complement)

def CouncilorsBills(councilor_id, bill_id, priproposer, petition):
    c.execute('''
        INSERT INTO bills_councilors_bills(councilor_id, bill_id, priproposer, petition)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (councilor_id, bill_id)
        DO UPDATE
        SET priproposer = %s, petition = %s
    ''', (councilor_id, bill_id, priproposer, petition, priproposer, petition))

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

for f in sorted(glob.glob('../../data/*/bills-*.json')):
    if int(re.search('bills-(\d+).json', f).group(1)) < int(election_year):
        continue
    print f
    county_abbr = f.split('/')[-2]
    f_election_year = re.search('-(\d+)\.json', f).group(1)
    county = common.county_abbr2string(county_abbr)
    county_abbr3 = common.county2abbr3(county)
    dict_list = json.load(open(f))
    for bill in dict_list:
        bill['county'] = county
        bill.update({'uid': u'%s-%s' % (bill['county'], bill['id'])})
        Bill(bill)
        for key, priproposer, petition in [('proposed_by', 0, False), ('petitioned_by', -1, True)]:
            for i, name in enumerate(bill.get(key, [])):
                name = common.normalize_person_name(name)
                name = re.sub(u'副?議長', '', name)
                if name:
                    # councilor in bill might not on this election_year
                    id, created = common.get_or_create_councilor_uid(c, dict(zip(['name', 'county', 'election_year', 'constituency'], [name, county, bill['election_year'], None])), create=False)
                    if id:
                        detail_id = common.getDetailIdFromUid(c, id, bill['election_year'], county)
                        CouncilorsBills(detail_id, bill['uid'], i==priproposer, petition)
        update_sponsor_param(bill['uid'])
        bill_party_diversity(bill['uid'])
    # Update bills_party_diversity of People
    for councilor_id in councilors(f_election_year, county):
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

# bills proposed_by city hall record on mayor
c.execute('''
    SELECT uid, county, election_year
    FROM mayors_terms
    WHERE election_year = %s
''', [election_year])
key = [desc[0] for desc in c.description]
for row in c.fetchall():
    person = dict(zip(key, row))
    c.execute('''
        SELECT b.uid
        FROM bills_bills b
        LEFT JOIN bills_councilors_bills bc ON b.uid = bc.bill_id
        WHERE b.county = %s and b.election_year = %s and bc.bill_id IS NULL and type != '人民請願案' and type != '議員提案' and type != '臨時動議案'
        order by b.proposed_by
    ''', [person['county'], person['election_year']])
    for bill in c.fetchall():
        c.execute('''
            INSERT INTO bills_mayors_bills(mayor_id, bill_id)
            VALUES (%s, %s)
            ON CONFLICT (mayor_id, bill_id)
            DO NOTHING
        ''', (person['uid'], bill[0]))
conn.commit()
print 'Update mayors bills done'
