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
    allowed_domains = ["www.ntcc.gov.tw"]
    start_urls = ["http://www.ntcc.gov.tw/webc/html/rep/index.aspx"]
    download_delay = 0.5

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), '../../data/cand-moi-county-control-2018.json'), 'r') as infile:
            self.ref = {re.sub(u'[\s　]', '', person['idname']): person for person in json.loads(infile.read()) if person['cityname'] == u'南投縣'}

    def parse(self, response):
        for url in response.xpath(u'//area[contains(@href, "district")]/@href').extract():
            yield scrapy.Request(urljoin(response.url, url.split('&')[0]), callback=self.parse_profile)

    def parse_profile(self, response):
        constituency, district = response.xpath('//select[@id="keyin5_list_select"]/option[@selected]/text()').extract_first().split(u'：')
        for node in response.xpath('//*[@class="list"]'):
            item = {}
            item['constituency'], item['district'] = constituency, district
            item['county'] = u'南投縣'
            item['election_year'] = '2014'
            item['term_start'] = '%s-12-25' % item['election_year']
            item['term_end'] = {'date': "2018-12-25"}
            item['in_office'] = True
            item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
            item['name'] = node.xpath(u'@id').extract_first()
            item['image'] = urljoin(response.url, node.xpath(u'descendant::img[@class="imgs2"]/@src').extract_first())
            item['gender'] = self.ref[item['name']]['sex']
            item['birth'] = GetDate(node.xpath(u'descendant::th[re:test(., "^出生：")]/following-sibling::td[1]/text()').extract_first())
            item['party'] = node.xpath(u'descendant::th[re:test(., "^政黨：")]/following-sibling::td[1]/text()').extract_first()
            item['title'] = node.xpath(u'*[@class="title"]/text()').extract_first().split('-')[-1]
            item['contact_details'] = []
            if self.ref[item['name']].get('officeadress'):
                item['contact_details'].append({
                    'label': u'通訊處',
                    'type': 'address',
                    'value': self.ref[item['name']]['officeadress']
                })
            if self.ref[item['name']].get('officetelphone'):
                item['contact_details'].append({
                    'label': u'連絡電話',
                    'type': 'voice',
                    'value': self.ref[item['name']]['officetelphone']
                })
            item['education'] = [x.strip() for x in node.xpath(u'descendant::th[re:test(., "^學歷：")]/following-sibling::td[1]/text()').extract() if x.strip()]
            item['experience'] = [x.strip() for x in node.xpath(u'descendant::th[re:test(., "^經歷：")]/following-sibling::td[1]/text()').extract() if x.strip()]
            yield item
