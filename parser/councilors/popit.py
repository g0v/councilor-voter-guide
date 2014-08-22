#!/usr/bin/env python
#coding:UTF-8
import sys
sys.path.append('../')
import json
import psycopg2
import requests
import subprocess
import db_settings
import local_settings


def counties():
    c.execute('''
        SELECT DISTINCT(county)
        FROM councilors_councilorsdetail
    ''')
    return c.fetchall()

def persons():
    c.execute('''
        SELECT uid as id, name, birth as birth_date
        FROM councilors_councilors
    ''')
    return [desc[0] for desc in c.description], c.fetchall()

def each_terms():
    c.execute('''
        SELECT councilor_id as person_id, election_year, name, gender, party, title as role, constituency, county, district, in_office, contact_details, term_start as start_date, cast(term_end::json->>'date' as date) as end_date, education, experience, remark, image, links, platform, param
        FROM councilors_councilorsdetail
    ''')
    return [desc[0] for desc in c.description], c.fetchall()

conn = db_settings.con()
c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
site_name = 'test-tw'
organizations_id = {}
for county in counties():
    organization = '%s議會' % county[0]
    r = requests.get('http://%s.popit.mysociety.org/api/v0.1/search/organizations?q=name:"%s"' % (site_name, organization))
    if r.json()['result']:
        organizations_id[county[0]] = r.json()['result'][0]['id']
    else:
        r = requests.post('http://%s.popit.mysociety.org/api/v0.1/organizations/' % site_name, data={'name': organization}, auth=(local_settings.EMAIL, local_settings.PASSWORD))
        organizations_id[county[0]] = r.json()['result']['id']

columns, persons = persons()
for person in persons:
    break
    r = requests.get('http://%s.popit.mysociety.org/api/v0.1/search/persons?q=id:"%s"' % (site_name, person['id']))
    if not r.json()['result']:
        r = requests.post('http://%s.popit.mysociety.org/api/v0.1/persons/' % site_name, data=dict(zip(columns, person)), auth=(local_settings.EMAIL, local_settings.PASSWORD))
        print r.text
        print 'person'

columns, terms = each_terms()
for term in terms:
    if term['start_date'] and term['end_date']:
        r = requests.get('http://%s.popit.mysociety.org/api/v0.1/search/memberships?q=person_id:"%s" AND organization_id:"%s" AND start_date:"%s" AND end_date:"%s"' % (site_name, term['person_id'], organizations_id[term['county']], term['start_date'], term['end_date']))
        print r.text
        print r.status_code
        if not r.json()['result']:
            payload = dict(zip(columns, term))
            payload.pop('links')
            payload['organization_id'] = organizations_id[term['county']]
            r = requests.post('http://%s.popit.mysociety.org/api/v0.1/memberships/' % site_name, data=payload, auth=(local_settings.EMAIL, local_settings.PASSWORD))
            print r.text
