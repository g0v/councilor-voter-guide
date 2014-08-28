#!/usr/bin/env python
#coding:UTF-8
import sys
sys.path.append('../')
import psycopg2
import requests
import db_settings
import local_settings


conn = db_settings.con()
c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
site_name = 'taiwan'

r = requests.get('http://%s.popit.mysociety.org/api/v0.1/persons/' % site_name)
persons = r.json()['result']
while(True):
    for person in persons:
        print requests.delete('http://%s.popit.mysociety.org/api/v0.1/persons/%s' % (site_name, person['id']))
    if r.json().get('next_url'):
        r = requests.get(r.json()['next_url'])
        persons = r.json()['result']
    else:
        break

r = requests.get('http://%s.popit.mysociety.org/api/v0.1/memberships/' % site_name)
persons = r.json()['result']
while(True):
    for person in persons:
        print requests.delete('http://%s.popit.mysociety.org/api/v0.1/memberships/%s' % (site_name, person['id']))
    if r.json().get('next_url'):
        r = requests.get(r.json()['next_url'])
        persons = r.json()['result']
    else:
        break
