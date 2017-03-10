# -*- coding: utf-8 -*-
import re
import os
import json
import urllib
from urlparse import urljoin
import scrapy


class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.mcc.gov.tw"]
    start_urls = ["http://www.mcc.gov.tw/home.php"]
    download_delay = 0.5

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'constituency.json'), 'r') as infile:
            self.constituency = json.loads(infile.read())
        with open(os.path.join(os.path.dirname(__file__), '../../data/cand-moi-county-control-2018.json'), 'r') as infile:
            self.ref = {re.sub(u'[\s　]', '', person['idname']): person for person in json.loads(infile.read()) if person['cityname'] == u'苗栗縣'}

    def parse(self, response):
        yield scrapy.Request(urljoin(response.url, response.xpath(u'(//img[@alt="本屆議員"]/parent::a)[1]/@href').extract_first()), callback=self.parse_current_ad)

    def parse_current_ad(self, response):
        for node in response.xpath(u'//a[re:test(@title, "第\S+選區")]'):
            yield scrapy.Request(urljoin(response.url, node.xpath('@href').extract_first()), callback=self.parse_profile, dont_filter=True, meta={'constituency': node.xpath('text()').extract_first().strip()})

    def parse_profile(self, response):
        for node in response.xpath('//table[@id="table98"]'):
            item = {}
            item['constituency'] = response.request.meta['constituency']
            item['district'] = self.constituency[item['constituency']]
            item['county'] = u'苗栗縣'
            item['election_year'] = '2014'
            item['term_start'] = '%s-12-25' % item['election_year']
            item['term_end'] = {'date': "2018-12-25"}
            item['in_office'] = True
            item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
            item['name'] = node.xpath(u'normalize-space((descendant::td)[1]/text())').extract_first()
            item['image'] = urljoin(response.url, node.xpath(u'(ancestor::td[1]/preceding-sibling::td)[1]/descendant::img[1]/@src').extract_first())
            item['gender'] = self.ref[item['name']]['sex']
            item['party'] = self.ref[item['name']]['partymship']
            item['title'] = self.ref[item['name']]['posiname']
            item['contact_details'] = []
            if self.ref[item['name']].get('officeadress'):
                item['contact_details'].append({
                    'label': u'服務處',
                    'type': 'address',
                    'value': self.ref[item['name']]['officeadress']
                })
            if self.ref[item['name']].get('officetelphone'):
                item['contact_details'].append({
                    'label': u'連絡電話',
                    'type': 'voice',
                    'value': self.ref[item['name']]['officetelphone']
                })
            item['education'] = [self.ref[item['name']]['education']]
            item['experience'] = [self.ref[item['name']]['profession']]
            yield item
