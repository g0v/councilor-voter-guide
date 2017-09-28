# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
import urllib
from urlparse import urljoin
import scrapy
import json

import common


class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.kmc.gov.tw"]
    start_urls = ["http://www.kmc.gov.tw/",]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    county = common.county_abbr2string(county_abbr)

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'constituency.json'), 'r') as infile:
            self.constituency = json.loads(infile.read())
        with open(os.path.join(os.path.dirname(__file__), '../../data/cand-moi-county-control-2018.json'), 'r') as infile:
            self.ref = {re.sub(u'[\s　]', '', person['idname']): person for person in json.loads(infile.read()) if person['cityname'] == u'基隆市'}

    def parse(self, response):
        return response.follow(response.xpath(u'//a[re:test(., "^議員資訊$")]/@href').extract_first(), callback=self.parse_list)

    def parse_list(self, response):
        for link in response.css('#speaker a::attr(href)'):
            yield response.follow(link, callback=self.parse_profile)

    def parse_profile(self, response):
        item = {}
        item['election_year'] = self.election_year
        item['county'] = self.county
        item['in_office'] = True
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': '2018-12-24'}
        print response.xpath(u'//p/span[re:test(., "\s+副?議(員|長)")]/text()').extract_first()
        item['name'], item['title'] = response.xpath(u'//p/span[re:test(., "\s+副?議(員|長)")]/text()').extract_first().split()
        item['gender'] = self.ref[item['name']]['sex']
        item['constituency'] = response.xpath('//td/text()').re(u'選區：\s*(.+)')[0].strip()
        item['district'] = self.constituency[item['constituency']]
        item['image'] = urljoin(response.url, response.xpath(u'//p/img/@src').extract_first())
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        item['party'] = response.xpath('//td/text()').re(u'政黨：\s*(.+)')[0].strip()
        item['birth'] = common.ROC2AD(response.xpath('//td/text()').re(u'出生日期：\s*(.+)')[0])
        website = response.xpath('//td/text()').re(u'網站連結：\s*(.+)')
        if website:
            item['links'].append({'url': website[0].strip(), 'note': u'個人網站'})
        item['contact_details'] = []
        contact_mappings = {
            u'連絡電話': 'voice',
            u'傳真號碼': 'fax',
            u'服務處': 'address',
            u'電子郵件': 'email'
        }
        for label, name in contact_mappings.items():
            values = [x.strip() for x in response.xpath(u'//td[re:test(., "%s：")]/text()' % '\s*'.join(label)).re(u'%s：\s*(.+)\s*' % label) if x.strip()]
            for value in values:
                item['contact_details'].append({
                    'label': label,
                    'type': name,
                    'value': value
                })
        item['experience'] = [x.strip() for x in response.xpath(u'//img[contains(@src, "speaker0")]')[1].xpath('ancestor::tr/following-sibling::tr[1]//tr/td[1]/text()').extract() if x.strip()]
        item['platform'] = [x.strip() for x in response.xpath(u'//img[contains(@src, "speaker0")]')[2].xpath('ancestor::tr/following-sibling::tr[1]//tr/td[1]/text()').extract() if x.strip()]
        yield item
