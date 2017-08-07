# -*- coding: utf-8 -*-
import re
import json

from django.core.serializers.json import DjangoJSONEncoder
from django import template
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.utils.dateparse import parse_datetime

from councilors.models import CouncilorsDetail
from bills.models import Bills


register = template.Library()


@register.filter(name='str2datetime')
def str2datetime(value):
    return parse_datetime(value)

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
def suggestions_offical_link(value, arg=None):
    maps = {
        u'臺北市': 'http://www.dbas.taipei.gov.tw/ct.asp?xItem=69201832&ctNode=31636&mp=120001',
        u'新竹市': 'http://dep-auditing.hccg.gov.tw/auditing/ch/home.jsp?id=46&parentpath=0,3',
        u'新北市': 'http://www.bas.ntpc.gov.tw/content/?parent_id=10067',
        u'桃園市': 'http://dbas.tycg.gov.tw/home.jsp?id=10199&parentpath=0,125,10197","http://dbas.tycg.gov.tw/home.jsp?id=10199&parentpath=0,125,10197',
        u'基隆市': 'http://civil.klcg.gov.tw/tw/Subject/ThemesServiceLi?ClassId=080A0D00',
        u'新竹縣': 'http://w3.hsinchu.gov.tw/infr_events/default.html#',
        u'苗栗縣': 'https://www.miaoli.gov.tw/cht/service_12.php',
        u'宜蘭縣': 'http://bgacst.e-land.gov.tw/News.aspx?n=70CDE68772BADADF&sms=6846E7E9DD40C190',
        u'臺中市': 'http://www.taichung.gov.tw/lp.asp?CtNode=25800&CtUnit=1064&BaseDSD=7&mp=1001D',
        u'彰化縣': 'http://accounting.chcg.gov.tw/07other/other01_con.asp?topsn=3367&data_id=14766',
        u'南投縣': 'http://www.nantou.gov.tw/big5/download.asp?dptid=376480000AU250000&cid=1724',
        u'雲林縣': 'http://www.yunlin.gov.tw/from/index-1.asp?m=2&m1=5&m2=142&id=111',
        u'嘉義縣': 'http://accounting.cyhg.gov.tw/News.aspx?n=8C5F83E8BF3FAB1A&sms=C56331427D07F11D',
        u'嘉義市': 'http://www.chiayi.gov.tw/web/account/main_13.asp',
        u'花蓮縣': 'http://www1.hl.gov.tw/ousv/parliament/index.asp',
        u'臺東縣': 'http://www.taitung.gov.tw/News.aspx?n=E316EA4999034915&sms=A9DCC80FC8CC7601',
        u'臺南市': 'http://www.tainan.gov.tw/tainan/Grants.asp?nsub=A6C400',
        u'高雄市': 'https://dbaskmg.kcg.gov.tw/business3.php?type=128',
        u'屏東縣': 'http://www.pthg.gov.tw/Cus_PublicInfo_List.aspx?n=0D6573E9ED3D2B78&pptype=7&ppsubtype=%E5%B0%8D%E8%AD%B0%E5%93%A1%E5%BB%BA%E8%AD%B0%E4%BA%8B%E9%A0%85%E8%BE%A6%E7%90%86%E6%83%85%E5%BD%A2%E8%A1%A8',
        u'連江縣': 'http://w3.matsu.gov.tw/2008web/statistical_data/statistical.php?cat=14',
        u'金門縣': 'http://web.kinmen.gov.tw/Layout/sub_F/News_NewsList.aspx?path=13448&DepID=10&LanguageType=1&CategoryID=885&DepartmentID=10',
        u'澎湖縣': 'https://www.penghu.gov.tw/ch/home.jsp?serno=201111070049&mserno=201111070038&contlink=ap/bulletin01.jsp&level3=Y&serno3=201111070053'
    }
    if arg == 'all':
        return maps.items()
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
        u'臺北市': 'http://www.tcc.gov.tw/',
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
        u'臺南市': 'http://www.tncc.gov.tw/',
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
