# -*- coding: utf-8 -*-
import re
import scrapy
import urllib
from urlparse import urljoin


class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.mtcc.gov.tw"]
    start_urls = ["http://www.mtcc.gov.tw/cu_legislator.html"]
    download_delay = 0.5

    def parse(self, response):
        for url in response.css('a.text-constituency').xpath('@href').extract():
            yield scrapy.Request(urljoin(response.url, url), callback=self.parse_profile)

    def parse_profile(self, response):
        item = {}
        item['election_year'] = '2014'
        item['county'] = u'連江縣'
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': '2018-12-25'}
        item['in_office'] = True
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        title_node = response.xpath(u'//tr[1]/td[re:test(., "^(議長|副議長|議員)")]')[-1]
        item['name'] = title_node.xpath('following-sibling::td[last()-1]/text()').extract_first().strip()
        item['title'] = title_node.xpath('text()').extract_first().strip()
        item['image'] = urljoin(response.url, title_node.xpath('following-sibling::td[last()]/descendant::img[1]/@src').extract_first())
        item['gender'] = response.xpath(u'//td[re:test(., "^性別")]')[-1].xpath('following-sibling::td[last()]/text()').extract_first().strip()
        item['party'] = response.xpath(u'//td[re:test(., "^黨籍")]')[-1].xpath('following-sibling::td[last()]/text()').extract_first().strip()
        item['constituency'], item['district'] = response.xpath(u'//td[re:test(., "^選區")]')[-1].xpath('following-sibling::td[last()]/text()').extract_first().strip(u'）').split(u'（')
        item['contact_details'] = []
        contact_mappings = {
            u'服務處電話': 'voice',
            u'服務處地址': 'address'
        }
        for label, name in contact_mappings.items():
            values = [x.strip() for x in response.xpath(u'//td[re:test(., "^%s")]' % label)[-1].xpath('following-sibling::td[last()]/text()').extract() if x.strip()]
            for value in values:
                item['contact_details'].append({
                    'label': label,
                    'type': name,
                    'value': value
                })
        item['education'] = [x.strip() for x in response.xpath(u'//td[re:test(., "^學歷")]')[-1].xpath('following-sibling::td[last()]/text()').extract() if x.strip()]
        if len(item['education']) == 1:
            item['education'] = item['education'][0].split(u'、')
        item['experience'] = [x.strip() for x in response.xpath(u'//td[re:test(., "^簡經歷")]')[-1].xpath('following-sibling::td/descendant::span/text()').extract() if x.strip()]
        item['platform'] = []
        platform_node = response.xpath(u'//td[re:test(., "^政見")]')[-1].xpath('following-sibling::td[last()]')
        for line in platform_node.xpath('descendant::tr'):
            item['platform'].append(''.join(line.xpath('descendant::*/text()').extract()))
        if item['platform'] == []:
            item['platform'] = [x.strip() for x in platform_node.xpath('descendant::*/text()').extract() if x.strip()]
        yield item
