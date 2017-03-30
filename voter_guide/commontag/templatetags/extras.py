# -*- coding: utf-8 -*-
import re
import json
from django.core.serializers.json import DjangoJSONEncoder
from django import template
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from councilors.models import CouncilorsDetail
from bills.models import Bills


register = template.Library()

@register.filter(name='select_county_reverse_url')
def select_county_reverse_url(value, arg):
    return reverse('%s:%s' % (value, value), kwargs={'county': arg})

@register.filter(name='each_county_remark')
def each_county_remark(value):
    maps = {
        u'桃園市': [
            u'找不到議案的資料來源，歡迎一起幫忙找，<a href="http://www.tycc.gov.tw/">議會官網</a>',
            u'出缺席紀錄處理中',
        ],
        u'新北市': [
            u'新北市議會出缺席為2012-09-05到現在的紀錄，2012-09-05之前的會議紀錄找不到記名的出缺席名單，<a href="http://www.ntp.gov.tw/content/information/information04.aspx">詳見議會官網</a>',
        ],
        u'臺中市': [
            u'臺中市議會除了第一次會議，其餘紀錄找不到記名的出缺席名單，<a href="http://www.tccc.gov.tw/govknowledge/know_docview.asp?id={A3251160-17E2-4B5B-9F99-1A985453159A}&wfid=23&info=1837">詳見議會官網</a>',
        ],
        u'彰化縣': [
            u'彰化縣議會找不到記名的出缺席名單和記名表決，<a href="http://www.chcc.gov.tw/">詳見議會官網</a>',
        ],
        u'嘉義市': [
            u'嘉義市議會找不到記名的出缺席名單和記名表決，<a href="http://www.cycc.gov.tw/form/index.asp?m=2&m1=7&m2=23">詳見議會官網</a>',
        ],
        u'嘉義縣': [
            u'嘉義縣議會找不到記名的出缺席名單和記名表決，<a href="http://www.cyscc.gov.tw/chinese/FormDownLoad_2.aspx?p=4&n=48">詳見議會官網</a>',
        ],
        u'新竹縣': [
            u'新竹縣議會找不到記名的出缺席名單和記名表決，<a href="http://www.hcc.gov.tw/">詳見議會官網</a>',
        ],
        u'新竹市': [
            u'新竹市議會找不到記名的出缺席名單和記名表決，<a href="http://www.hsinchu-cc.gov.tw/">詳見議會官網</a>',
        ],
        u'苗栗縣': [
            u'苗栗縣議會找不到議案、記名的出缺席名單和記名表決，<a href="http://www.mcc.gov.tw/">詳見議會官網</a>',
        ],
        u'南投縣': [
            u'南投縣議會找不到記名的出缺席名單和記名表決，<a href="http://www.ntcc.gov.tw/">詳見議會官網</a>',
        ],
        u'花蓮縣': [
            u'花蓮縣議會找不到記名的出缺席名單和記名表決，<a href="http://www.hlcc.gov.tw/">詳見議會官網</a>',
        ],
        u'臺東縣': [
            u'臺東縣議會找不到記名的出缺席名單和記名表決，<a href="http://www.taitungcc.gov.tw/">詳見議會官網</a>',
        ],
        u'屏東縣': [
            u'屏東縣議會找不到記名的出缺席名單和記名表決，<a href="http://www.ptcc.gov.tw/">詳見議會官網</a>',
        ],
        u'連江縣': [
            u'連江縣議會找不到記名的出缺席名單和記名表決，<a href="http://www.mtcc.gov.tw/">詳見議會官網</a>',
        ],
        u'金門縣': [
            u'金門縣議會找不到記名的出缺席名單和記名表決，<a href="http://www.kmcc.gov.tw/">詳見議會官網</a>',
        ],
    }
    return '<br>'.join(maps.get(value, ''))

@register.filter(name='suggestions_offical_link')
def suggestions_offical_link(value):
    maps = {
        u'臺北市': 'http://www.dbas.taipei.gov.tw/ct.asp?xItem=69201832&ctNode=31636&mp=120001',
        u'高雄市': 'http://dbaskmg.kcg.gov.tw/business3.php?type=128',
        u'新竹市': 'http://dep-auditing.hccg.gov.tw/web/SG?pageID=27404&FP=42985',
    }
    return maps.get(value, '')

@register.filter(name='distinct_district')
def distinct_district(value, arg):
    return CouncilorsDetail.objects.filter(county=value, election_year=arg).exclude(district='').values_list('district', flat=True).distinct()

@register.filter(name='vote_result')
def vote_result(value, arg):
    attribute = {
        'Passed': {
            'td_bgcolor': u'CCFF99',
            'cht': u'通過'
        },
        'Not Passed': {
            'td_bgcolor': u'FF99CC',
            'cht': u'不通過'
        }
    }
    if attribute.get(value):
        return attribute.get(value).get(arg)

@register.filter(name='election_year_range')
def election_year_range(value):
    election_years = ['1969', '1973', '1977', '1981', '1985', '1989', '1994', '1998', '2002', '2006', '2010', '2014', '2018']
    for i in range(0, len(election_years)):
        if election_years[i] == value:
            return '%s~%s' % (value, election_years[i+1])
    election_years = ['2009', '2014', '2018']
    for i in range(0, len(election_years)):
        if election_years[i] == value:
            return '%s~%s' % (value, election_years[i+1])

@register.filter(name='mod')
def mod(value, arg):
    return value % arg

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

@register.filter(name='multiply')
def subtract(value, arg):
    return value * arg

@register.filter(name='percentage')
def percentage(value, arg):
    if arg:
        try:
            return "{0:.1f}".format(value * 100.0 / arg)
        except Exception, e:
            print e
    else:
        return 0

@register.filter(name='divide')
def divide(value, arg):
    if arg:
        try:
            return "{0:.2f}".format(value / arg)
        except Exception, e:
            print e
    else:
        return 0

@register.filter(name='as_json')
def as_json(data):
    return mark_safe(json.dumps(data, cls=DjangoJSONEncoder))

@register.filter(name='replace')
def replace(value, arg):
    if arg:
        for word in arg.split():
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            value = pattern.sub('<font style="background-color: #FFFF66;">'+word+'</font>', value)
        return value
    else:
        return value

@register.filter(name='county_urls')
def county_urls(value):
    maps = {
        u'基隆市': 'http://www.kmc.gov.tw/',
        u'新北市': 'http://www.ntp.gov.tw/',
        u'台北市': 'http://www.tcc.gov.tw/',
        u'桃園市': 'http://www.tycc.gov.tw/',
        u'新竹市': 'http://www.hsinchu-cc.gov.tw/',
        u'新竹縣': 'http://www.hcc.gov.tw/',
        u'苗栗縣': 'http://www.mcc.gov.tw/',
        u'臺中市': 'http://www.tccc.gov.tw/',
        u'彰化縣': 'http://www.chcc.gov.tw/',
        u'雲林縣': 'http://www.ylcc.gov.tw/',
        u'南投縣': 'http://www.ntcc.gov.tw/',
        u'嘉義市': 'http://www.cycc.gov.tw/',
        u'嘉義縣': 'http://www.cyscc.gov.tw/',
        u'台南市': 'http://www.tncc.gov.tw/',
        u'高雄市': 'http://www.kcc.gov.tw/',
        u'屏東縣': 'http://www.ptcc.gov.tw/',
        u'宜蘭縣': 'http://www.ilcc.gov.tw/',
        u'花蓮縣': 'http://www.hlcc.gov.tw/',
        u'臺東縣': 'http://www.taitungcc.gov.tw/',
        u'澎湖縣': 'http://www.phcouncil.gov.tw/',
        u'連江縣': 'http://www.mtcc.gov.tw/',
        u'金門縣': 'http://www.kmcc.gov.tw/',
    }
    return maps.get(value, '')
