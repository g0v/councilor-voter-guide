# -*- coding: utf-8 -*-
import re
import os
import json
import urllib
from urlparse import urljoin
import scrapy


class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.ylcc.gov.tw"]
    start_urls = [
         "http://www.ylcc.gov.tw"
    ]

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'constituency.json'), 'r') as infile:
            self.constituency = json.loads(infile.read())
        with open(os.path.join(os.path.dirname(__file__), '../../data/cand-moi-county-control-2018.json'), 'r') as infile:
            self.ref = {re.sub(u'[\s　]', '', person['idname']): person for person in json.loads(infile.read()) if person['cityname'] == u'雲林縣'}

    def parse(self, response):
        for node in response.xpath(u'//a[@title="議員介紹"]/ancestor::li[1]/descendant::li/a'):
            yield scrapy.Request(urljoin(response.url, node.xpath(u'@href').extract_first()), callback=self.parse_profile, meta={"constituency": node.xpath('text()').extract_first()})

    def parse_profile(self, response):
        for candidate in response.xpath("//*[@class='word_orange']/ancestor::td[1]"):
            item = {}
            item['name'] = candidate.xpath(".//*[@class='word_orange']/text()").extract_first()
            item['image'] = urljoin(response.url, candidate.xpath(u'preceding::img[contains(@alt, "照片")]/@src').extract()[-1])
            item['election_year'] = '2014'
            item['county'] = u'雲林縣'
            item['term_start'] = '%s-12-25' % item['election_year']
            item['term_end'] = {'date': '2018-12-25'}
            item['in_office'] = True
            item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
            item["constituency"] = response.request.meta["constituency"]
            item['district'] = self.constituency[item["constituency"]]
            item['contact_details'] = []
            lines = [x.strip() for x in candidate.xpath('.//text()').extract()[1:] if x.strip()]
            for i in range(0, len(lines), 2):
                if re.search(u'學\s*歷', lines[i]):
                    item['education'] = lines[i+1].split(u'、')
                if re.search(u'經\s*歷', lines[i]):
                    item['experience'] = lines[i+1].split(u'、')
                if re.search(u'黨\s*籍', lines[i]):
                    item['party'] = lines[i+1]
                if re.search(u'服\s*務\s*處\s*電\s*話', lines[i]):
                    item['contact_details'].append({'type': 'voice', 'label': u'電話', 'value': lines[i+1]})
                if re.search(u'服\s*務\s*處\s*傳\s*真', lines[i]):
                    item['contact_details'].append({'type': 'fax', 'label': u'傳真', 'value': lines[i+1]})
                if re.search(u'服\s*務\s*處\s*地\s*址', lines[i]):
                    item['contact_details'].append({'type': 'address', 'label': u'通訊處', 'value': lines[i+1]})
                if re.search(u'電\s*子\s*信\s*箱', lines[i]):
                    item['contact_details'].append({'type': 'email', 'label': u'電子信箱', 'value': lines[i+1]})
            item['gender'] = self.ref[item['name']]['sex']
            item['title'] = self.ref[item['name']]['posiname']
            yield item
