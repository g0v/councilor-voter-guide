#! /usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import glob


for file in glob.glob('../../meeting_minutes/*/*/*'):
    print(file)
    county_abbr, election_year = file.split('/')[-3:-1]
    file_name, ext = file.split('/')[-1].split('.')
    output_path = '../../data/%s/meeting_minutes/%s/' % (county_abbr, election_year)
    output_file = '%s%s.txt' % (output_path, file_name)
    retcode = subprocess.call('mkdir -p %s' % output_path, shell=True)
    if ext == 'pdf':
        cmd = 'pdftotext -nopgbrk %s %s' % (file, output_file)
    elif ext == 'doc':
        cmd = 'textract %s -o %s' % (file, output_file)
    elif ext == 'docx':
        cmd = 'textract %s -o %s' % (file, output_file)
    retcode = subprocess.call(cmd, shell=True)
