#!/usr/bin/python
# -*- coding: utf-8 -*
import json
import codecs


def write_file(data, file_name):
    file = codecs.open(file_name, 'w', encoding='utf-8')
    file.write(data)
    file.close()

for file_name in ['taipei_councilor-11.json', 'taipei_meeting_minutes.json']:
    objs = json.load(open(file_name))
    dump_data = json.dumps(objs, sort_keys=True, indent=4, ensure_ascii=False)
    write_file(dump_data, 'pretty_format/%s' % file_name)

#objs = json.load(open('taipei_meeting_minutes.json'))
#dump_data = json.dumps(objs, sort_keys=True, indent=4, ensure_ascii=False)
#write_file(dump_data, 'pretty_format/taipei_meeting_minutes-11.json')
