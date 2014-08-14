#!/usr/bin/env python
#coding:UTF-8
import json
import subprocess

d = {
    "person_id": "53eafef2cc89eebc09c11cd2",
    "organization_id": "53ec53086370cbbf3f29db13"
}
person = json.dumps(d)
print person
#cmd = 'curl --user twly.tw@gmail.com:c3oRZ0am --request POST  --header "Accept: application/json" --header "Content-Type: application/json" --data \'%s\' http://test-tw.popit.mysociety.org/api/v0.1/persons' % person
cmd = 'curl --user twly.tw@gmail.com:c3oRZ0am --request POST --header "Accept: application/json" --header "Content-Type: application/json" --data \'%s\' http://test-tw.popit.mysociety.org/api/v0.1/memberships/' % person
retcode = subprocess.call(cmd, shell=True)

