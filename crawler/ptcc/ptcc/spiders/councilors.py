# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.selector import Selector
from ptcc.items import Councilor
import urllib
from urlparse import urljoin
from scrapy.http import Request
import os
import json

class Spider(scrapy.Spider):
    name = "councilors"
    '''
    allowed_domains = ["localhost"]
    start_urls = [
         "http://localhost/p1_index.html"
    ]
    '''
    allowed_domains = ["www.ptcc.gov.tw"]
    start_urls = [
         "http://www.ptcc.gov.tw/?Page=Persional&Guid=1c445ed1-8f2f-4c7f-75f6-6d6aafa3516e"
    ]
    download_delay = 0.5

    def __init__(self):
        fh=open(os.path.join(os.path.dirname(__file__), 'constituency.json'), 'r')
        self.constituency = json.loads(fh.read())

    def parse(self, response):
        sel= Selector(response)
        index_table = sel.xpath(".//td[@class='list borderleft']")
        candidates = index_table.xpath(".//a/@href")
        for candidate in candidates:
            url = urljoin(response.url, candidate.extract())
            yield Request(url, callback=self.parse_profile)

    def parse_profile(self, response):
        sel = Selector(response)
        item = Councilor()

        item['election_year'] = '2009'
        item['county'] = u'屏東縣'
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': '2014-12-25'}
        item['in_office'] = True
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        img_url = sel.xpath(".//td[@bgcolor='#E8E8E8']/img/@src").extract()[0]
        item['image'] = urljoin(response.url, img_url)
        name_parent = sel.xpath(".//td[@bgcolor='#E8E8E8']/../..")
        name = name_parent.xpath(".//tr/td/text()").extract()[0].replace(u'議員：','')
        item['name'] = name
        print item['name']
        item['contact_details'] = []
        details = sel.xpath(".//td[@class='list']/..")
        for detail in details:
            info=detail.xpath(".//td/text()")
            if info[0].re(u'[\s]*政[\s]*黨[\s]*'):
                item['party']=info[1].extract().strip()
            if info[0].re(u'[\s]*選[\s]*區[\s]*'):
                item['constituency'] = re.sub(u'[(（].*', '', info[1].extract()).strip()
                item['district'] = self.constituency[item['constituency']]
            if info[0].re(u'[\s]*性[\s]*別[\s]*'):
                item['gender'] = info[1].extract().strip()
            if info[0].re(u'[\s]*聯[\s]*絡[\s]*處[\s]*'):
                address = info[1].extract().strip()
                if address:
                    item['contact_details'].append({'type': 'address', 'label': u'通訊處', 'value': address})
            if info[0].re(u'[\s]*電[\s]*話[\s]*'):
                phone = info[1].extract().strip()
                if phone:
                    item['contact_details'].append({'type': 'voice', 'label': u'電話', 'value': phone})
            if info[0].re(u'[\s]*傳[\s]*真[\s]*'):
                fax = info[1].extract().strip()
                if fax:
                    item['contact_details'].append({'type': 'fax', 'label': u'傳真', 'value': fax})
            if info[0].re(u'[\s]*電[\s]*子[\s]*郵[\s]*件[\s]*'):
                email = info[1].extract().strip()
                if email:
                    item['contact_details'].append({'type': 'email', 'label': u'電子信箱', 'value': email})
            if info[0].re(u'[\s]*簡[\s]*介[\s]*'):
                item['platform'] = [x.strip() for x in info.extract()[1:]]
        return item
