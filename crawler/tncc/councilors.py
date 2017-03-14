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
        return '%04d-%02d-%02d' % (int(matchTerm.group('year')), int(matchTerm.group('month')), int(matchTerm.group('day')))
    else:
        return None

class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.tncc.gov.tw"]
    start_urls = ["http://www.tncc.gov.tw/tnccp2/default.asp",]
    download_delay = 0.5

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), '../../data/cand-moi-direct-control-2018.json'), 'r') as infile:
            self.ref = {re.sub(u'[\s　]', '', person['idname']): person for person in json.loads(infile.read()) if person['cityname'] == u'臺南市'}

    def parse(self, response):
        for node in response.css('.style1'):
            region = node.xpath('text()').extract_first().strip(')').split(u'(')
            for person in node.xpath('ancestor::tr[1]/following-sibling::tr/descendant::a | following-sibling::a[1]'):
                item = {}
                item['name'] = person.xpath('text()').extract_first()
                item['constituency'], item['district'] = region
                item['district'] = item['district'].replace(u'.', u'、')
                yield scrapy.Request(urljoin(response.url, person.xpath('@href').extract_first()), callback=self.parse_profile, meta={'item': item})

    def parse_profile(self, response):
        item = response.meta['item']
        item['county'] = u'臺南市'
        item['election_year'] = '2014'
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': "2018-12-25"}
        item['in_office'] = True
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        image_src = response.xpath('//*[re:test(@src, "^/warehouse/")]/@src').extract_first()
        item['image'] = urljoin(response.url, urllib.quote(image_src.encode(response.encoding)))
        item['title'] = self.ref[item['name']]['posiname']
        item['gender'] = self.ref[item['name']]['sex']
        item['birth'] = GetDate(response.xpath(u'//td[re:test(., "出生：")]')[-1].xpath('text()').extract_first().strip().split(u'：')[-1])
        item['party'] = response.xpath(u'//td[re:test(., "黨\s*籍：")]')[-1].xpath('text()').extract_first().strip().split(u'：')[-1]
        link = re.sub(u'\s|　', '', response.xpath(u'//td[re:test(., "FaceBook：")]/descendant::a[1]/@href').extract_first())
        if link:
            item['links'].append({'url': link, 'note': u'FaceBook'})
        item['contact_details'] = []
        contact_mappings = {
            u'電話': 'voice',
            u'通訊處': 'address',
        }
        for label, name in contact_mappings.items():
            values = [x.strip().split(u'：')[-1] for x in response.xpath(u'//td[re:test(., "%s")]' % '\s*'.join(label))[-1].xpath('text()').extract() if x.strip().split(u'：')[-1]]
            for value in values:
                item['contact_details'].append({
                    'label': label,
                    'type': name,
                    'value': value
                })
        values = [x.strip() for x in response.xpath(u'//td[re:test(., "電子信箱：")]')[-1].xpath('descendant::a/text()').extract() if x.strip()]
        for value in values:
            item['contact_details'].append({
                'label': u'電子信箱',
                'type': 'email',
                'value': value
            })
        item['education'] = [x.strip() for x in response.xpath(u'//div[re:test(., "^學[\s　]*歷$")]')[-1].xpath('following-sibling::div[1]/text()').extract() if x.strip()]
        item['experience'] = [x.strip() for x in response.xpath(u'//div[re:test(., "^經[\s　]*歷$")]')[-1].xpath('following-sibling::div[1]/text()').extract() if x.strip()]
        item['platform'] = [x.strip() for x in response.xpath(u'//div[re:test(., "^政[\s　]*見$")]')[-1].xpath('following-sibling::div[1]/text()').extract() if x.strip()]
        yield item
