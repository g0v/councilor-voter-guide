# -*- coding: utf-8 -*-
import re
import os
import json
import urllib
from urlparse import urljoin
import scrapy


def GetDate(text):
    matchTerm = re.search(u'''
        (?P<year>[\d]+)[\s]*(年|[./-])[\s]*
        (?P<month>[\d]+)[\s]*(月|[./-])[\s]*
        (?P<day>[\d]+)
    ''', text, re.X)
    if matchTerm:
        return '%04d-%02d-%02d' % (int(matchTerm.group('year'))+1911, int(matchTerm.group('month')), int(matchTerm.group('day')))
    else:
        return None

class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.phcouncil.gov.tw"]
    start_urls = ["http://www.phcouncil.gov.tw/mop1.php"]
    download_delay = 1

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), '../../data/cand-moi-county-control-2018.json'), 'r') as infile:
            self.ref = {re.sub(u'[\s　]', '', person['idname']): person for person in json.loads(infile.read()) if person['cityname'] == u'澎湖縣'}

    def parse(self, response):
        for i, area in enumerate(response.xpath(u'//*[contains(text(), "應選")]')):
            district = area.xpath('text()').extract_first().strip('(').split(')')[0]
            for person in area.xpath('(following::table)[1]/descendant::a'):
                item = {}
                item['name'] = re.search(u'(?:議長|副議長)?(\S+)\s+議員', person.xpath('string(parent::*)').extract_first()).group(1)
                item['constituency'] = u'第%d選區' % i
                item['district'] = district
                yield scrapy.Request(urljoin(response.url, person.xpath('@href').extract_first()), callback=self.parse_profile, meta={'item': item})

    def parse_profile(self, response):
        item = response.meta['item']
        item['image'] = urljoin(response.url, response.xpath(u'//img[contains(@src, "attachments/")]/@src').extract_first())
        item['birth'] = GetDate(response.xpath(u'string(//*[contains(text(), "出生年月日")]/parent::*)').extract_first())
        if self.ref.get(item['name']):
            item['constituency'] = self.ref[item['name']]['eareaname'].strip(u'澎湖縣')
        item['party'] = self.ref.get(item['name'], {}).get('partymship', '')
        item['gender'] = self.ref.get(item['name'], {}).get('sex', '')
        item['title'] = self.ref.get(item['name'], {}).get('posiname', '')
        item['county'] = u'澎湖縣'
        item['election_year'] = '2014'
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': "2018-12-25"}
        item['in_office'] = True
        item['contact_details'] = []
        if self.ref.get(item['name'], {}).get('officeadress'):
            item['contact_details'].append({
                'label': u'服務處',
                'type': 'address',
                'value': self.ref[item['name']]['officeadress']
            })
        if self.ref.get(item['name'], {}).get('officetelphone'):
            item['contact_details'].append({
                'label': u'連絡電話',
                'type': 'voice',
                'value': self.ref[item['name']]['officetelphone']
            })
        if self.ref.get(item['name'], {}).get('education'):
            item['education'] = self.ref.get(item['name'], {}).get('education', '').split()
        else:
            item['education'] = [x.strip(u':').strip() for x in response.xpath(u'//*[contains(text(), "學歷")]/parent::*/text()').extract() if x.strip(u':').strip()]
        if self.ref.get(item['name'], {}).get('profession'):
            item['experience'] = self.ref.get(item['name'], {}).get('profession', '').split()
        else:
            item['experience'] = [x.strip(u'：').strip() for x in response.xpath(u'//*[contains(text(), "經歷")]/parent::*/text()').extract() if x.strip(u'：').strip()]
        yield item
