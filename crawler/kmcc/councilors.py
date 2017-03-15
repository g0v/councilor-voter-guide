# -*- coding: utf-8 -*-
import re
import os
import json
import urllib
from urlparse import urljoin
import scrapy


class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.kmcc.gov.tw"]
    start_urls = ["http://www.kmcc.gov.tw/men/men.aspx"]
    download_delay = 0.5

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), '../../data/cand-moi-county-control-2018.json'), 'r') as infile:
            self.ref = {re.sub(u'[\s　]', '', person['idname']): person for person in json.loads(infile.read()) if person['cityname'] == u'金門縣'}

    def parse(self, response):
        for area in response.css('div.area'):
            region = [x.strip() for x in area.xpath('text()').extract_first().split('/')]
            for person in area.xpath('following-sibling::div[1]/a'):
                item = {}
                item['name'] = person.xpath('text()').extract_first()
                item['constituency'], item['district'] = region
                yield scrapy.Request(urljoin(response.url, person.xpath('@href').extract_first()), callback=self.parse_profile, meta={'item': item})

    def parse_profile(self, response):
        item = response.meta['item']
        item['gender'] = self.ref[item['name']]['sex']
        item['title'] = self.ref[item['name']]['posiname']
        item['county'] = u'金門縣'
        item['election_year'] = '2014'
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': "2018-12-25"}
        item['in_office'] = True
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        item['image'] = urljoin(response.url, response.xpath('//img[contains(@src, "images/men")]/@src').extract_first())
        maps = dict(zip([re.sub(u'[\s　：:]', '', x) for x in response.css('.mentextabout_left').xpath('text()').extract()], response.css('.mentextabout_right').xpath('text()').extract()))
        item['party'] = maps[u'政黨']
        item['contact_details'] = []
        if maps.get(u'服務地址'):
            item['contact_details'].append({
                'label': u'服務地址',
                'type': 'address',
                'value': maps[u'服務地址']
            })
        if maps.get(u'聯絡電話'):
            item['contact_details'].append({
                'label': u'聯絡電話',
                'type': 'voice',
                'value': maps[u'聯絡電話']
            })
        item['education'] = [x.strip() for x in response.xpath(u'//div[re:test(., "^學[\s　]*歷")]')[-1].xpath('following::ol[1]/descendant::*/text()').extract() if x.strip()]
        item['experience'] = [x.strip() for x in response.xpath(u'//div[re:test(., "^經[\s　]*歷")]')[-1].xpath('following::ol[1]/descendant::*/text()').extract() if x.strip()]
        item['platform'] = [x.strip() for x in response.xpath(u'//div[re:test(., "^政[\s　]*見")]')[-1].xpath('following::ol[1]/descendant::*/text()').extract() if x.strip()]
        yield item
