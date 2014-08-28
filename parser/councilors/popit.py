#!/usr/bin/env python
#coding:UTF-8
import sys
sys.path.append('../')
import psycopg2
import requests
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
    return c.fetchall()

def each_terms():
    c.execute('''
        SELECT councilor_id as person_id, election_year, name, gender, party, title as role, constituency, county, district, in_office, contact_details as contact, term_start as start_date, cast(term_end::json->>'date' as date) as end_date, education, experience, remark, image, platform, param
        FROM councilors_councilorsdetail
        where contact_details is not null
    ''')
    return c.fetchall()

conn = db_settings.con()
c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
site_name = 'taiwan'
organizations_id = {}

# Get the id of city council if exist, if not, create it
for row in counties():
    organization = '%s議會' % row['county']
    r = requests.get('http://%s.popit.mysociety.org/api/v0.1/search/organizations?q=name:"%s"' % (site_name, organization))
    print r.text
    if r.status_code == 200:
        if r.json()['result']:
            organizations_id[row['county']] = r.json()['result'][0]['id']
        else:
            r = requests.post('http://%s.popit.mysociety.org/api/v0.1/organizations/' % site_name, data={'name': organization}, auth=(local_settings.EMAIL, local_settings.PASSWORD))
            organizations_id[row['county']] = r.json()['result']['id']
            print r.text

# Create person if not exist
for person in persons():
    break
    print person
    r = requests.get('http://%s.popit.mysociety.org/api/v0.1/search/persons?q=id:"%s"' % (site_name, person['id']))
    print r.text
    if r.status_code == 200:
        if not r.json()['result']:
            r = requests.post('http://%s.popit.mysociety.org/api/v0.1/persons/' % site_name, data=person, auth=(local_settings.EMAIL, local_settings.PASSWORD))
            print r.text
        else:
            r = requests.put('http://%s.popit.mysociety.org/api/v0.1/persons/%s' % (site_name, r.json()['result'][0]['id']), data=person, auth=(local_settings.EMAIL, local_settings.PASSWORD))
            print r.text

# Create the memberships if not exist, else update it
for term in each_terms():
    print term
    if term['start_date']:
        r = requests.get('http://%s.popit.mysociety.org/api/v0.1/search/memberships?q=person_id:"%s" AND organization_id:"%s" AND start_date:"%s"' % (site_name, term['person_id'], organizations_id[term['county']], term['start_date']))
        term['organization_id'] = organizations_id[term['county']]
        print r.text
        if r.status_code == 200:
            if not r.json()['result']:
                r = requests.post('http://%s.popit.mysociety.org/api/v0.1/memberships/' % site_name, data=term, auth=(local_settings.EMAIL, local_settings.PASSWORD))
                print r.text
            else:
                r = requests.delete('http://%s.popit.mysociety.org/api/v0.1/memberships/%s' % (site_name, r.json()['result'][0]['id']), data=term, auth=(local_settings.EMAIL, local_settings.PASSWORD))
                print r.text
    else:
        raw_input()
