# -*- coding: utf-8 -*-
import re


def election_year(county):
    return '2014'

def meeting_minutes_output_path(county_abbr, election_year):
    return '../../meeting_minutes/%s/%s/' % (county_abbr, election_year)

def ROC2AD(text):
    matchTerm = re.search(u'''
        (?P<year>[\d]+)[\s]*(?:年|[-/.])[\s]*
        (?P<month>[\d]+)[\s]*(?:月|[-/.])[\s]*
        (?P<day>[\d]+)
    ''', text, re.X)
    if matchTerm:
        return '%04d-%02d-%02d' % (int(matchTerm.group('year'))+1911, int(matchTerm.group('month')), int(matchTerm.group('day')))
