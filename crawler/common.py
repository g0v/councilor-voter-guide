# -*- coding: utf-8 -*-
import re


def storage_domain():
    return 'https://drsgjxdg6zyfq.cloudfront.net'

def election_year(county):
    return '2014'

def county_abbr2string(abbr):
    return {
        'ntp': u'新北市',
        'tcc': u'臺北市',
        'tycc': u'桃園市',
        'kmc': u'基隆市',
        'ilcc': u'宜蘭縣',
        'hcc': u'新竹縣',
        'hsinchucc': u'新竹市',
        'mcc': u'苗栗縣',
        'tccc': u'臺中市',
        'chcc': u'彰化縣',
        'ylcc': u'雲林縣',
        'ntcc': u'南投縣',
        'cyscc': u'嘉義縣',
        'cycc': u'嘉義市',
        'tncc': u'臺南市',
        'kcc': u'高雄市',
        'ptcc': u'屏東縣',
        'hlcc': u'花蓮縣',
        'taitungcc': u'臺東縣',
        'mtcc': u'連江縣',
        'kmcc': u'金門縣',
        'phcouncil': u'澎湖縣'
    }[abbr]

def headers(county):
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }

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
