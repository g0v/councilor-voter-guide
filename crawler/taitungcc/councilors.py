# -*- coding: utf-8 -*-
import re
import urllib
from urlparse import urljoin
import scrapy


class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.taitungcc.gov.tw"]
    start_urls = ["http://www.taitungcc.gov.tw/OurTeam.aspx"]
    download_delay = 0.5

    def parse(self, response):
        for node in response.css('.team').xpath('descendant::dt'):
            for a_tag in node.xpath('following-sibling::dd[1]/descendant::a'):
                item = {}
                item['constituency'] = node.xpath('text()').extract_first()
                item['district'] = node.xpath('span/text()').extract_first()
                item['name'] = a_tag.xpath('text()').extract_first()
                yield scrapy. Request(urljoin(response.url, a_tag.xpath('@href').extract_first()), callback=self.parse_profile, meta={'item': item})

    def parse_profile(self, response):
        item = response.meta['item']
        item['county'] = u'臺東縣'
        item['election_year'] = '2014'
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': "2018-12-25"}
        item['in_office'] = True
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        website = response.xpath(u'//i[re:test(., "網站連結")]/parent::a[1]/@href').extract_first()
        if website:
            item['links'].append({'url': website, 'note': u'個人網站'})
        item['image'] = urljoin(response.url, response.css('.person_pic').xpath('@src').extract_first())
        item['gender'] = response.xpath(u'//p[re:test(., "性[\s　]*別：")]/span[1]/text()').extract_first()
        item['party'] = response.xpath(u'//p[re:test(., "黨[\s　]*籍：")]/span[1]/text()').extract_first()
        item['contact_details'] = []
        contact_mappings = {
            u'電話': 'voice',
            u'地址': 'address'
        }
        for label, name in contact_mappings.items():
            values = [x.strip() for x in response.css('.card').xpath(u'p[re:test(., "%s：")]/span/text()' % u'[\s　]*'.join(label)).extract() if x.strip()]
            for value in values:
                item['contact_details'].append({
                    'label': label,
                    'type': name,
                    'value': value
                })
        item['education'] = [x.strip() for x in response.xpath(u'//dt[re:test(., "學[\s　]*歷")]/following-sibling::dd[1]/text()').extract() if x.strip()]
        item['experience'] = [x.strip() for x in response.xpath(u'//dt[re:test(., "經[\s　]*歷")]/following-sibling::dd[1]/text()').extract() if x.strip()]
        item['platform'] = [x.strip() for x in response.xpath(u'//dt[re:test(., "政[\s　]*見")]/following-sibling::dd[1]/text()').extract() if x.strip()]
        yield item
