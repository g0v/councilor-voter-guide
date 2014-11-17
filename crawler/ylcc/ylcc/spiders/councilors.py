# -*- coding: utf-8 -*-
import re
import os
import json
import urllib
from urlparse import urljoin
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from ylcc.items import Councilor


class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.ylcc.gov.tw"]
    start_urls = [
         "http://www.ylcc.gov.tw/index.php"
    ]
    '''
    allowed_domains = ["localhost"]
    start_urls = [
         "http://localhost/y4.html"
    ]
    '''
    def __init__(self):
        fh=open(os.path.join(os.path.dirname(__file__), 'constituency.json'), 'r')
        self.constituency = json.loads(fh.read())

    def parse(self, response):
        for idx in range(1, 7):
            url='http://www.ylcc.gov.tw/index.php?inner=member_precinct%d' % idx
            print url
            yield Request(url, callback=self.parse_profile, meta={"constituency": u'第%d選區' % idx})
        '''
        patterns=['y6']
        for pattern in patterns:
            url='http://localhost/'+ pattern + '.html'
            print url
            profile = Request(url, callback=self.parse_profile)
            result.append(profile)
        return result
        '''

    def parse_profile(self, response):
        sel = Selector(response)
        itemresult=[]
        for candidate in sel.xpath("//span[@class='word_orange']/ancestor::td[1] | //p[@class='word_orange']/ancestor::td[1]"):
            #print candidate.extract().encode('utf8')
            item = Councilor()
            item['name'] = candidate.xpath(".//*[@class='word_orange']/text()").extract()[0]
            print item['name']
            item['image'] = urljoin(response.url, candidate.xpath(u'preceding::img[contains(@alt, "照片")]/@src').extract()[-1])
            item['election_year'] = '2009'
            item['county'] = u'雲林縣'
            item['term_start'] = '%s-12-25' % item['election_year']
            item['term_end'] = {'date': '2014-12-25'}
            item['in_office'] = True
            item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
            item["constituency"] = response.request.meta["constituency"]
            item['district'] = self.constituency[item["constituency"]]
            item['contact_details']=[]
            lines = [x.strip() for x in candidate.xpath('.//text()').extract()[1:] if x.strip() != '']
            for i in range(0, len(lines), 2):
                if re.search(u'學\s*歷', lines[i]):
                    item['education'] = [lines[i+1]]
                if re.search(u'經\s*歷', lines[i]):
                    item['experience'] = [lines[i+1]]
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
            itemresult.append(item)
        return itemresult
