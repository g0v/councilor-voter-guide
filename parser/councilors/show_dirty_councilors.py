#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import db_settings
import common


def Councilors(councilor):
    councilor['former_names'] = councilor.get('former_names', [])
    variants = set()
    for variant in [(u'温', u'溫'), (u'黄', u'黃'), (u'寳', u'寶'), (u'真', u'眞'), (u'福', u'褔'), (u'鎭', u'鎮'), (u'姸', u'妍'), (u'市', u'巿'), (u'衛', u'衞'), (u'館', u'舘'), (u'峰', u'峯'), (u'群', u'羣'), (u'啓', u'啟'), (u'鳳', u'鳯'), (u'冗', u'宂'), ]:
        variants.add(re.sub(variant[0], variant[1], councilor['name']))
        variants.add(re.sub(variant[1], variant[0], councilor['name']))
    councilor['identifiers'] = list((variants | set(councilor['former_names']) | {councilor['name'], re.sub(u'[\w‧’]]', '', councilor['name']), re.sub(u'\W', '', councilor['name']).lower(), }) - {''})
    councilor['former_names'] = '\n'.join(councilor['former_names'])
    complement = {"birth": None}
    complement.update(councilor)
    c.execute('''
        INSERT INTO councilors_councilors(uid, name, birth, former_names, identifiers)
        VALUES (%(uid)s, %(name)s, %(birth)s, %(former_names)s, %(identifiers)s)
        ON CONFLICT (uid)
        DO UPDATE
        SET name = %(name)s, birth = %(birth)s, former_names = %(former_names)s, identifiers = %(identifiers)s
    ''', complement)

conn = db_settings.con()
c = conn.cursor()
# update all councilor's identifiers
c.execute('''
    SELECT *
    FROM councilors_councilors
    WHERE identifiers is null
''')
key = [desc[0] for desc in c.description]
for row in c.fetchall():
    person = dict(zip(key, row))
    person['name'] = person['name'].decode('utf-8')
    Councilors(person)
conn.commit()

# clean dirty councilors
c.execute('''
    SELECT identifiers
    FROM councilors_councilors
    GROUP BY identifiers
    HAVING count(*) > 1
''')
for row in c.fetchall():
    identifiers = row[0]
    c.execute('''
        SELECT cd.councilor_id, cd.name, cd.election_year, cd.county, cd.constituency FROM councilors_councilors c, councilors_councilorsdetail cd WHERE c.identifiers = %s AND c.uid = cd.councilor_id
    ''', [identifiers])
    key = [desc[0] for desc in c.description]
    details = c.fetchall()
    if len(details) > 1: # 同 identifiers 的人有兩個以上屆期
        uids = set([detail[0] for detail in details])
        if len(uids) > 1: # 同 identifiers 的各屆期的人有不同的 uid
            for i, detail in enumerate(details):
                print i
                person = dict(zip(key, detail))
                for k, v in person.items():
                    print k, v
