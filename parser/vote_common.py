# -*- coding: utf-8 -*-
import re
import json
import common


# --> conscience vote
def party_Decision_List(c, party, election_year):
    c.execute('''
        select vote_id, avg(decision)
        from votes_councilors_votes
        where decision is not null and councilor_id in (select id from councilors_councilorsdetail where party = %s and election_year = %s)
        group by vote_id
    ''', (party, election_year))
    return c.fetchall()

def personal_Decision_List(c, party, vote_id, election_year):
    c.execute('''
        select councilor_id, decision
        from votes_councilors_votes
        where decision is not null and vote_id = %s and councilor_id in (select id from councilors_councilorsdetail where party = %s and election_year = %s)
    ''', (vote_id, party, election_year))
    return c.fetchall()

def party_List(c, election_year, county):
    c.execute('''
        select party, count(*)
        from councilors_councilorsdetail
        where election_year = %s and county = %s and party != '無黨籍'
        group by party
    ''', (election_year, county))
    return c.fetchall()

def conflict_vote(c, conflict, vote_id):
    c.execute('''
        update votes_votes
        set conflict = %s
        where uid = %s
    ''', (conflict, vote_id))

def conflict_voter(c, conflict, councilor_id, vote_id):
    c.execute('''
        update votes_councilors_votes
        set conflict = %s
        where councilor_id = %s and vote_id = %s
    ''', (conflict, councilor_id, vote_id))

def conscience_vote(c, election_year, county):
    for party, count in party_List(c, election_year, county):
        if count > 2:
            for vote_id, avg_decision in party_Decision_List(c, party, election_year):
                # 黨的decision平均值如不為整數，表示該表決有人脫黨投票
                if int(avg_decision) != avg_decision:
                    conflict_vote(c, True, vote_id)
                    # 同黨各立委的decision與黨的decision平均值相乘如小於(相反票)等於(棄權票)零，表示脫黨投票
                    for councilor_id, personal_decision in personal_Decision_List(c, party, vote_id, election_year):
                        if personal_decision*avg_decision <= 0:
                            conflict_voter(c, True, councilor_id, vote_id)
# <-- conscience vote

# --> not voting & vote results
def vote_list(c, county):
    c.execute('''
        select vote.uid, sitting.election_year, sitting.date
        from votes_votes vote, sittings_sittings sitting
        where vote.sitting_id = sitting.uid and sitting.county = %s
    ''', (county,))
    return c.fetchall()

def delete_not_in_terms_voting_record(c, vote_id, vote_ad, vote_date):
    c.execute('''
        delete from votes_councilors_votes
        where id in (
            select vl.id
            from votes_votes v, votes_councilors_votes vl, councilors_councilorsdetail l
            where v.uid = vl.vote_id and l.id = vl.councilor_id and l.election_year = %s and (l.term_start > %s or cast(l.term_end::json->>'date' as date) <= %s) and v.uid = %s
        )
    ''', (vote_ad, vote_date, vote_date, vote_id))

def not_voting_list(c, county, vote_id, vote_ad, vote_date):
    c.execute('''
        select id
        from councilors_councilorsdetail
        where election_year = %s and county = %s and term_start <= %s and cast(term_end::json->>'date' as date) > %s and id not in (select councilor_id from votes_councilors_votes where vote_id = %s)
    ''', (vote_ad, county, vote_date, vote_date, vote_id))
    return c.fetchall()

def insert_not_voting_record(c, councilor_id, vote_id):
    c.execute('''
        INSERT INTO votes_councilors_votes(councilor_id, vote_id)
        SELECT %s, %s
        WHERE NOT EXISTS (SELECT councilor_id, vote_id FROM votes_councilors_votes WHERE councilor_id = %s AND vote_id = %s)
    ''', (councilor_id, vote_id, councilor_id, vote_id))

def get_vote_results(c, vote_id):
    c.execute('''
        select
            count(*) total,
            sum(case when decision isnull then 1 else 0 end) not_voting,
            sum(case when decision = 1 then 1 else 0 end) agree,
            sum(case when decision = 0 then 1 else 0 end) abstain,
            sum(case when decision = -1 then 1 else 0 end) disagree
        from votes_councilors_votes
        where vote_id = %s
    ''', (vote_id,))
    return [desc[0] for desc in c.description], c.fetchone() # return column name and value

def update_vote_results(c, uid, results):
    c.execute('''
        select json_agg(row)
        from (
            select decision, json_agg(party_list) as party_list, sum(count)
            from (
                select decision, json_build_object('party', party, 'councilors', councilors, 'count', json_array_length(councilors)) as party_list, json_array_length(councilors) as count
                from (
                    select decision, party, json_agg(detail) as councilors
                    from (
                        select decision, party, json_build_object('name', name, 'councilor_id', councilor_id) as detail
                        from (
                            select
                                case
                                    when vl.decision = 1 then '贊成'
                                    when vl.decision = -1 then '反對'
                                    when vl.decision = 0 then '棄權'
                                    when vl.decision isnull then '沒投票'
                                end as decision,
                                l.party,
                                l.name,
                                l.councilor_id
                            from councilors_councilorsdetail l, votes_votes v , votes_councilors_votes vl, sittings_sittings s
                            where v.uid = %s and v.uid = vl.vote_id and vl.councilor_id = l.id and v.sitting_id = s.uid
                        ) _
                    ) __
                group by decision, party
                order by decision, party
                ) ___
            ) ____
        group by decision
        order by sum desc
        ) row
    ''', [uid])
    decisions = c.fetchone()[0]
    if results['agree'] > results['disagree']:
        result = 'Passed'
    else:
        result = 'Not Passed'
    c.execute('''
        UPDATE votes_votes
        SET result = %s, results = %s
        WHERE uid = %s
    ''', (result, decisions, uid))

def not_voting_and_results(c, county):
    for vote_id, vote_ad, vote_date in vote_list(c, county ):
        for councilor_id in not_voting_list(c, county, vote_id, vote_ad, vote_date):
            insert_not_voting_record(c, councilor_id, vote_id)
        delete_not_in_terms_voting_record(c, vote_id, vote_ad, vote_date)
        key, value = get_vote_results(c, vote_id)
        update_vote_results(c, vote_id, dict(zip(key, value)))
# <-- not voting & vote results end

def person_vote_param(c, county):
    c.execute('''
        SELECT
            councilor_id,
            COUNT(*) total,
            SUM(CASE WHEN conflict = True THEN 1 ELSE 0 END) "conflict",
            SUM(CASE WHEN decision isnull THEN 1 ELSE 0 END) not_voting,
            SUM(CASE WHEN decision = 1 THEN 1 ELSE 0 END) agree,
            SUM(CASE WHEN decision = 0 THEN 1 ELSE 0 END) abstain,
            SUM(CASE WHEN decision = -1 THEN 1 ELSE 0 END) disagree
        FROM votes_councilors_votes
        GROUP BY councilor_id
    ''', [county])
    response = c.fetchall()
    for r in response:
        param = dict(zip(['total', 'conflict', 'not_voting', 'agree', 'abstain', 'disagree'], r[1:]))
        c.execute('''
            UPDATE councilors_councilorsdetail
            SET param = (COALESCE(param, '{}'::jsonb) || %s::jsonb)
            WHERE county = %s AND id = %s
        ''', (json.dumps({'votes_decision_statistics': param}), county, r[0]))

def person_attendance_param(c, county):
    c.execute('''
        SELECT
            councilor_id,
            COUNT(*) total,
            SUM(CASE WHEN category = 'CS' AND status = 'absent' THEN 1 ELSE 0 END) absent
        FROM councilors_attendance
        GROUP BY councilor_id
    ''')
    response = c.fetchall()
    for r in response:
        param = dict(zip(['total', 'absent'], r[1:]))
        c.execute('''
            UPDATE councilors_councilorsdetail
            SET param = (COALESCE(param, '{}'::jsonb) || %s::jsonb)
            WHERE county = %s AND id = %s
        ''', (json.dumps({'attendance_statistics': param}), county, r[0]))

# not attend complement
def sitting_list(c, county):
    c.execute('''
        select uid, election_year, date
        from sittings_sittings
        where county = %s
    ''', (county,))
    return c.fetchall()

def not_attend_list(c, county, sitting_id, election_year, sitting_date):
    c.execute('''
        select id
        from councilors_councilorsdetail
        where election_year = %s and county = %s and term_start <= %s and cast(term_end::json->>'date' as date) > %s and id not in (select councilor_id from councilors_attendance where sitting_id = %s)
    ''', (election_year, county, sitting_date, sitting_date, sitting_id))
    return c.fetchall()

def insert_not_attend_record(c, councilor_id, sitting_id):
    c.execute('''
        SELECT category
        FROM councilors_attendance
        WHERE sitting_id = %s AND category != ''
        LIMIT 1
    ''', (sitting_id, ))
    r = c.fetchone()
    category = r[0] if r else ''
    c.execute('''
        INSERT into councilors_attendance(councilor_id, sitting_id, category, status)
        SELECT %s, %s, %s, %s
        WHERE NOT EXISTS (SELECT 1 FROM councilors_attendance WHERE councilor_id = %s AND sitting_id = %s)
    ''', (councilor_id, sitting_id, category, 'absent', councilor_id, sitting_id))

def delete_not_in_terms_attend_record(c, sitting_id, election_year, sitting_date):
    c.execute('''
        delete from councilors_attendance
        where id in (
            select a.id
            from councilors_attendance a, councilors_councilorsdetail l
            where l.id = a.councilor_id and l.election_year = %s and (l.term_start > %s or cast(l.term_end::json->>'date' as date) <= %s) and a.sitting_id = %s
        )
    ''', (election_year, sitting_date, sitting_date, sitting_id))

def not_attend_complement(c, county):
    for sitting_id, election_year, sitting_date in sitting_list(c, county ):
        for councilor_id in not_attend_list(c, county, sitting_id, election_year, sitting_date):
            insert_not_attend_record(c, councilor_id, sitting_id)
#   delete_not_in_terms_attend_record(c, sitting_id, election_year, sitting_date)
# <-- not attend complement end
