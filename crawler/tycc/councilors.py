# -*- coding: utf-8 -*-
import os
import json
import re
import urllib
from urlparse import urljoin
import scrapy
import logging


class Spider(scrapy.Spider):
    name = "councilors"
    start_urls = ["http://www.tycc.gov.tw/page.aspx?wtp=1&wnd=204", ]
    download_delay = 0.5

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), '../../data/cand-moi-direct-control-2018.json'), 'r') as infile:
            self.ref = {re.sub(u'[\s　]', '', person['idname']): person for person in json.loads(infile.read()) if person['cityname'] == u'桃園市'}

    def parse(self, response):
        urls = response.xpath('//map/area[@alt]/@href').extract()
        for url in urls:
            yield scrapy.Request(urljoin(response.url, url), callback=self.parse_selection_index)

    def parse_selection_index(self, response):
        selected_count = len(response.xpath('//*[@id="ctl00_ContentPlaceHolder1_Members1_DDL_AREA"]/option[@selected]/preceding-sibling::option')) + 1
        constituency = u'第%d選區' % selected_count
        urls = response.xpath('//img/parent::a[@alt]/@href').extract()
        for url in urls:
            yield scrapy.Request(urljoin(response.url, url), callback=self.parse_profile, meta={'constituency': constituency})

    def parse_profile(self, response):
        item = {}
        item['constituency'] = response.meta['constituency']
        item['county'] = u'桃園市'
        item['election_year'] = '2014'
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': '2018-12-25'}
        item['in_office'] = True
        item['name'], item['title'] = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_Members1_LB_MEM_NAME"]/text()').extract_first().split()
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        item['party'] = self.ref[item['name']]['partymship']
        item['gender'] = self.ref[item['name']]['sex']
        img_url = response.xpath('//img[@class="memImg"]/@src').extract_first()
        item['image'] = urljoin(response.url, urllib.quote(img_url.encode('utf8')))
        region = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_Members1_LB_MEM_AREA"]/text()').extract_first().split()
        # e.g. "平地原住民" vs "第一選區 桃園區"
        item['district'] = region[1] if len(region) > 1 else region[0]
        item['education'] = [x.strip() for x in response.xpath('//*[@id="ctl00_ContentPlaceHolder1_Members1_LB_MEM_SCHOOL"]/text()').extract() if x.strip()]
        item['experience'] = [x.strip() for x in response.xpath('//*[@id="ctl00_ContentPlaceHolder1_Members1_LB_MEM_WORK"]/text()').extract() if x.strip()]

        fb_links = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_Members1_LB_MEM_FACEBOOK"]/descendant::a/@href').extract()
        for fb_link in fb_links:
            item['links'].append({'url': fb_link, 'note': u'臉書'})

        item['contact_details'] = []
        emails = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_Members1_LB_MEM_EMAIL"]/descendant::a/@href').extract()
        for email in emails:
            item['contact_details'].append({
                'label': u'電子信箱',
                'type': 'email',
                'value': email.lstrip('mailto://')
            })
        addresses = response.xpath('//text()').re(u'服務處：(.*)')
        for address in addresses:
            item['contact_details'].append({
                'label': u'服務處',
                'type': 'address',
                'value': address.strip()
            })
        voices = response.xpath('//text()').re(u'電話:([\d -]*)')
        for voice in voices:
            item['contact_details'].append({
                'label': u'電話',
                'type': 'voice',
                'value': voice.strip()
            })
        faxs = response.xpath('//text()').re(u'傳真:([\d -]*)')
        for fax in faxs:
            item['contact_details'].append({
                'label': u'傳真',
                'type': 'fax',
                'value': fax.strip()
            })
        item['platform'] = [x.strip() for x in response.xpath('//*[@id="ctl00_ContentPlaceHolder1_Members1_LB_MEM_IDEA"]/text()').extract() if x.strip()]
        yield item
