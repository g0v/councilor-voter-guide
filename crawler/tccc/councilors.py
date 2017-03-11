# -*- coding: utf-8 -*-
import os
import re
import json
import urllib
from urlparse import urljoin
import scrapy


class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.tccc.gov.tw"]
    start_urls = ["http://www.tccc.gov.tw/main.asp?uno=16", ]
    download_delay = 0.5

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), '../../data/cand-moi-direct-control-2018.json'), 'r') as infile:
            self.ref = {re.sub(u'[\s　]', '', person['idname']): person for person in json.loads(infile.read()) if person['cityname'] == u'臺中市'}

    def parse(self, response):
        for node in response.xpath(u'//a[re:test(@title, "第\S+選區")]'):
            item = {'constituency': node.xpath('text()').extract_first().strip()}
            yield scrapy.Request(urljoin(response.url, node.xpath('@href').extract_first()), callback=self.parse_iframe, meta={'item': item})

    def parse_iframe(self, response):
        url = urljoin(response.url, response.xpath('//iframe[@name="wb_main"]/@src').extract_first())
        meta = response.request.meta
        return scrapy.Request(url, callback=self.parse_constituency, meta=meta)

    def parse_constituency(self, response):
        item = response.request.meta['item']
        item['district'] = response.xpath(u'normalize-space(string(//td[re:test(., "\[%s\]")]/following-sibling::td[1]))' % item['constituency']).extract_first()
        for url in response.xpath(u'//a[contains(@href, "wb_intro")]/@href').extract():
            yield scrapy.Request(urljoin(response.url, url), callback=self.parse_profile, meta={'item': item})

    def parse_profile(self, response):
        item = response.request.meta['item']
        item['county'] = u'臺中市'
        item['election_year'] = '2014'
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': "2018-12-25"}
        item['in_office'] = True
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        item['name'] = response.xpath(u'//td[re:test(., "%s")]/text()' % item['constituency']).extract()[-1].strip()
        item['image'] = urljoin(response.url, response.xpath(u'//*[@id="Layer2"]/descendant::img[re:test(@src, "^Conn/")]/@src').extract_first())
        item['gender'] = self.ref[item['name']]['sex']
        item['party'] = self.ref[item['name']]['partymship']
        item['title'] = self.ref[item['name']]['posiname']
        for value in response.xpath(u'//td[re:test(., "社群網站")]/following-sibling::td[1]/descendant::a/@href').extract():
            item['links'].append({
                'note': u'社群網站',
                'url': value
            })
        item['contact_details'] = []
        contact_mappings = {
            u'電話': 'voice',
            u'傳真': 'fax',
            u'地址': 'address'
        }
        for label, name in contact_mappings.items():
            values = [x.strip() for x in response.xpath(u'//td[re:test(., "%s：")]/following-sibling::td[1]/text()' % '\s*'.join(label)).re(u'%s：\s*(.+)\s*' % label) if x.strip()]
            for value in values:
                item['contact_details'].append({
                    'label': label,
                    'type': name,
                    'value': value
                })
        for value in response.xpath(u'//td[re:test(., "Email")]/following-sibling::td[1]/descendant::a/text()').extract():
            item['contact_details'].append({
                'label': 'E-mail',
                'type': 'email',
                'value': value
            })
        item['education'] = [x.strip() for x in response.xpath(u'//*[re:test(., "^學\s*歷$")]/ancestor::tr[2]/following-sibling::tr[1]/descendant::p/text()').extract() if x.strip()]
        item['experience'] = [x.strip() for x in response.xpath(u'//*[re:test(., "^經\s*歷$")]/ancestor::tr[2]/following-sibling::tr[1]/descendant::p/text()').extract() if x.strip()]
        item['platform'] = [x.strip() for x in response.xpath(u'//*[re:test(., "^政\s*見$")]/ancestor::tr[2]/following-sibling::tr[1]/descendant::p/text()').extract() if x.strip()]
        yield item
