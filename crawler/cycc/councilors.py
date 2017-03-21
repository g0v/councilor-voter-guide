# -*- coding: utf-8 -*-
import re
import os
import json
import urllib
from urlparse import urljoin
import scrapy


class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.cycc.gov.tw"]
    start_urls = [
         "http://www.cycc.gov.tw/index2.asp"
    ]

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), '../../data/cand-moi-county-control-2018.json'), 'r') as infile:
            self.ref = {re.sub(u'[\s　]', '', person['idname']): person for person in json.loads(infile.read()) if person['cityname'] == u'嘉義市'}

    def parse(self, response):
        yield scrapy.Request(urljoin(response.url, response.xpath(u'//img[@alt="本會議員"]/parent::a/@href').extract_first()), callback=self.parse_current_ad)

    def parse_current_ad(self, response):
        for node in response.xpath(u'//a[re:test(., "第\S+選區")]'):
            constituency = node.xpath(u'text()').extract_first()
            yield scrapy.Request(urljoin(response.url, node.xpath(u'@href').extract_first()), callback=self.parse_constituency, meta={'constituency': constituency})

    def parse_constituency(self, response):
        for url in response.xpath(u'//a[@class="link-news"]/@href').extract():
            yield scrapy.Request(urljoin(response.url, url), callback=self.parse_profile, meta=response.meta)
        for url in response.xpath(u'//a[@class="link-page"]/@href').extract():
            yield scrapy.Request(urljoin(response.url, url), callback=self.parse_pages, meta=response.meta)

    def parse_pages(self, response):
        for url in response.xpath(u'//a[@class="link-news"]/@href').extract():
            yield scrapy.Request(urljoin(response.url, url), callback=self.parse_profile, meta=response.meta)

    def parse_profile(self, response):
        item = {}
        item['county'] = u'嘉義市'
        item['election_year'] = '2014'
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': "2018-12-25"}
        item['in_office'] = True
        item['constituency'] = response.meta['constituency']
        item['name'] = re.sub(u'[\s　]', '', response.xpath(u'//*[@class="title1"]/text()').extract_first())
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        item['district'] = response.xpath(u'string(//th[re:test(., "個 人 網 站選[\s　]*區")]/following-sibling::td[1])').extract_first().strip()
        values = [x.strip() for x in response.xpath(u'string(//th[re:test(., "%s")]/following-sibling::td[1])' % u'[\s　]*'.join(u'個人網站')).extract() if x.strip()]
        for value in values:
            item['links'].append({
                'note': u'個人網站',
                'url': value
            })
        item['image'] = urljoin(response.url, urllib.quote(response.xpath(u'//img[@id="ADimg0"]/@src').extract_first().encode(response.encoding)))
        item['gender'] = self.ref[item['name']]['sex']
        item['party'] = self.ref[item['name']]['partymship']
        item['title'] = self.ref[item['name']]['posiname']
        item['district'] = response.xpath(u'string(//th[re:test(., "選[\s　]*區")]/following-sibling::td[1])').extract_first().strip()
        item['contact_details'] = []
        contact_mappings = {
            u'電話': 'voice',
            u'傳真': 'fax',
            u'地址': 'address',
            u'E-mail': 'email'
        }
        for label, name in contact_mappings.items():
            values = [x.strip() for x in response.xpath(u'string(//th[re:test(., "%s")]/following-sibling::td[1])' % u'[\s　]*'.join(label)).extract_first().split(u'、') if x.strip()]
            for value in values:
                item['contact_details'].append({
                    'label': label,
                    'type': name,
                    'value': value
                })
        item['education'] = [x.strip() for x in response.xpath(u'//th[re:test(., "學[\s　]*歷")]/following-sibling::td[1]/descendant-or-self::*/text()').extract() if x.strip()]
        item['experience'] = [x.strip() for x in response.xpath(u'//th[re:test(., "經[\s　]*歷")]/following-sibling::td[1]/descendant-or-self::*/text()').extract() if x.strip()]
        yield item
