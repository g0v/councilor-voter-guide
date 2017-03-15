# -*- coding: utf-8 -*-
import re
import os
import json
import scrapy
import urllib
from urlparse import urljoin

class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.ptcc.gov.tw"]
    start_urls = ["http://www.ptcc.gov.tw/?Page=Persional&Guid=1c445ed1-8f2f-4c7f-75f6-6d6aafa3516e"]
    download_delay = 0.5

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'constituency.json'), 'r') as infile:
            self.constituency = json.loads(infile.read())
        with open(os.path.join(os.path.dirname(__file__), '../../data/cand-moi-county-control-2018.json'), 'r') as infile:
            self.ref = {re.sub(u'[\s　]', '', person['idname']): person for person in json.loads(infile.read()) if person['cityname'] == u'屏東縣'}

    def parse(self, response):
        for candidate in response.css('.list.borderleft').xpath("a/@href"):
            url = urljoin(response.url, candidate.extract())
            yield scrapy.Request(url, callback=self.parse_profile)

    def parse_profile(self, response):
        item = {}
        item['election_year'] = '2014'
        item['county'] = u'屏東縣'
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': '2018-12-25'}
        item['in_office'] = True
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        for website in response.xpath(u'//td[re:test(., "^個人網站│")]')[-1].xpath('following-sibling::td[1]/descendant::a'):
            item['links'].append({'url': website.xpath('@href').extract_first(), 'note': website.xpath('text()').extract_first()})

        item['name'] = response.xpath(u'//td[re:test(., "議員：")]')[-1].xpath('text()').extract_first().strip(u'議員：').strip()
        img_url = response.xpath('//td[@bgcolor="#E8E8E8"]/img/@src').extract_first()
        item['image'] = urljoin(response.url, img_url)
        item['party'] = response.xpath(u'//td[re:test(., "^政[\s　]*黨")]')[-1].xpath('following-sibling::td[1]/text()').extract_first().strip()
        item['constituency'] = re.sub(u'[(（].*', '', response.xpath(u'//td[re:test(., "^選[\s　]*區")]')[-1].xpath('following-sibling::td[1]/text()').extract_first()).strip()
        item['district'] = self.constituency[item['constituency']]
        item['gender'] = response.xpath(u'//td[re:test(., "^性[\s　]*別")]')[-1].xpath('following-sibling::td[1]/text()').extract_first().strip().strip(u'性')
        item['contact_details'] = []
        contact_mappings = {
            u'電話': 'voice',
            u'傳真': 'fax',
            u'聯絡處': 'address',
            u'電子郵件': 'email',
        }
        for label, name in contact_mappings.items():
            values = [x.strip() for x in response.xpath(u'//td[re:test(., "^%s")]' % u'[\s　]*'.join(label))[-1].xpath('following-sibling::td[1]/text()').extract() if x.strip()]
            for value in values:
                item['contact_details'].append({
                    'label': label,
                    'type': name,
                    'value': value
                })
        item['platform'] = [x.strip() for x in response.xpath(u'//td[re:test(., "^簡[\s　]*介")]')[-1].xpath('following-sibling::td[1]/text()').extract() if x.strip()]
        yield item
