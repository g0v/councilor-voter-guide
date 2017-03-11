# -*- coding: utf-8 -*-
import os
import re
import json
import urllib
from urlparse import urljoin
import scrapy


class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.ilcc.gov.tw"]
    start_urls = ["http://www.ilcc.gov.tw/Html/H_05/H_05.asp", ]
    download_delay = 0.5

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), '../../data/cand-moi-county-control-2018.json'), 'r') as infile:
            self.ref = {re.sub(u'[\s　]', '', person['idname']): person for person in json.loads(infile.read()) if person['cityname'] == u'宜蘭縣'}

    def parse(self, response):
        areas = response.xpath(u'//table[contains(@summary, "議員列表")]')
        for area in areas:
            name = area.xpath('@summary').extract_first()
            area_info = re.match('(.*)\((.*)\).*', name).groups()
            urls = area.xpath('descendant::a/@href').extract()
            for i, url in enumerate(urls):
                url = url.encode(response.encoding)
                meta = {'area': area_info, 'cookiejar': "%s_%d" % (name, i)}
                yield scrapy.Request(urljoin(response.url, url), meta=meta, dont_filter=True, callback=self.parse_profile_frameset)

    def parse_profile_frameset(self, response):
        url = urljoin(response.url, response.xpath('//frame[@name="mainFrame"]/@src').extract_first())
        meta = response.request.meta
        return scrapy.Request(url, callback=self.parse_profile, meta=meta)

    def parse_profile(self, response):
        meta = response.request.meta
        item = {}
        item['contact_details'] = []
        item['election_year'] = '2014'
        item['term_end'] = {'date': '2018-12-25'}
        item['term_start'] = '%s-12-25' % item['election_year']
        item['in_office'] = True
        item['county'] =  u'宜蘭縣'
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        img_url = response.xpath('.//div[@id="Layer2"]/img/@src').extract_first()
        item['image'] = urljoin(response.url, img_url)
        if meta:
            item['constituency'], item['district'] = meta['area']
        item['name'] = response.xpath(u'normalize-space(string((//td[re:test(., "姓名")]/following-sibling::td)[1]))').extract_first().strip()
        item['party'] = response.xpath(u'normalize-space(string((//td[re:test(., "黨籍")]/following-sibling::td)[1]))').extract_first()
        item['education'] = response.xpath(u'normalize-space(string((//td[re:test(., "學歷")]/following-sibling::td)[1]))').extract()
        contact_mappings = {
            u'E-mail': 'email',
            u'服務處所電話': 'voice',
            u'服務處所': 'address'
        }
        for label, name in contact_mappings.items():
            values = [x.strip() for x in response.xpath(u'normalize-space(string((//td[re:test(., "%s")]/following-sibling::td)[1]))' % '\s*'.join(label)).extract() if x.strip()]
            for value in values:
                item['contact_details'].append({
                    'label': label,
                    'type': name,
                    'value': value
                })
        item['experience'] = [x.strip() for x in response.xpath(u'(//td[re:test(., "曾任")]/following-sibling::td)[1]/descendant::*/text()').extract_first().split('\r\n') if x.strip()]
        item['platform'] = [x.strip() for x in response.xpath(u'(//td[re:test(., "政見")]/following-sibling::td)[1]/descendant::*/text()').extract_first().split('\r\n') if x.strip()]
        item['gender'] = self.ref[item['name']]['sex']
        item['title'] = self.ref[item['name']]['posiname']
        yield item
