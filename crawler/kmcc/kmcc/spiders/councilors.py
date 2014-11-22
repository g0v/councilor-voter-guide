# -*- coding: utf-8 -*-
import re
import os
import json
import urllib
from urlparse import urljoin
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from kmcc.items import Councilor


class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.kmcc.gov.tw"]
    start_urls = ["http://www.kmcc.gov.tw/men/"]
    download_delay = 0.1

    def parse(self, response):
        for href in response.xpath('//a[contains(@href, "htm")]/@href').extract():
            yield Request(urljoin(response.url, href), callback=self.parse_profile)

    def parse_profile(self, response):
        item = Councilor()
        try:
            item['image'] = urljoin(response.url, response.xpath('//table[@id="table7"]/descendant::img/@src').extract()[0])
        except:
            return
        item['name'] = response.xpath('//title/text()').extract()[0].split('-')[-1].strip()
        item['county'] = u'金門縣'
        item['election_year'] = '2009'
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': "2014-12-25"}
        item['in_office'] = True
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        item['contact_details'] = []
        for node in response.xpath('//table[@id="table8"]/tr/td/descendant::font'):
            text = node.xpath('text()').extract()[0]
            text = re.sub(u'[　\s]', '', text)
            following_text = [x.strip() for x in node.xpath('following-sibling::text()').extract() if x.strip()]
            if re.search(u'政黨：', text):
                item['party'] = text.split(u'：')[-1]
            elif re.search(u'學歷：', text):
                item['education'] = following_text
            elif re.search(u'經歷：', text):
                item['experience'] = following_text
            elif re.search(u'服務地址：', text):
                item['contact_details'].append({"label" : u'地址', "type" : "address", "value" : text.split(u'：')[-1]})
            elif re.search(u'聯絡電話：', text):
                item['contact_details'].append({"label" : u'電話', "type" : "voice", "value" : text.split(u'：')[-1]})
        return Request(urljoin(response.url, response.xpath('//iframe/@src').extract()[0]), callback=self.parse_platform, meta={'item': item}, dont_filter=True)

    def parse_platform(self, response):
        item = response.meta['item']
        item['platform'] = [x.strip() for x in response.xpath('//li/text()').extract()]
        return item
