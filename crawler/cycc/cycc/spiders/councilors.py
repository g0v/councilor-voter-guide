# -*- coding: utf-8 -*-
import re
import os
import json
import urllib
from urlparse import urljoin
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from cycc.items import Councilor
from crawler_lib import parse

class Spider(scrapy.Spider):
    name = "councilors"
    '''
    allowed_domains = ["localhost"]
    start_urls = [
         "http://localhost/cy4_u.html"
    ]
    '''
    allowed_domains = ["www.cycc.gov.tw"]
    start_urls = [
         "http://www.cycc.gov.tw/form1/index-2.asp?"
    ]

    def __init__(self):
        pass

    def parse(self, response):
        # section 1
        result=[]
        for idx in range(1, 12):
            url='http://www.cycc.gov.tw/form1/index-2.asp?m=99&m1=4&m2=15&mode=1&id='+str(idx)
            profile = Request(url, callback=self.parse_profile, meta={'constituency': u'第1選區'})
            print url
            result.append(profile)

        for idx in range(12, 25):
            url='http://www.cycc.gov.tw/form1/index-2.asp?m=99&m1=4&m2=15&mode=2&id='+str(idx)
            profile = Request(url, callback=self.parse_profile, meta={'constituency': u'第2選區'})
            result.append(profile)

        return result

    def parse_profile(self, response):
        response = parse.get_decoded_response(response, 'Big5')
        #print response
        sel = Selector(response)
        item = Councilor()
        item['name'] = sel.xpath(".//span[@class='title1']/text()").extract()[0]
        print item['name']
        item['election_year'] = '2009'
        item['county'] = '嘉義市'
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': '2014-12-25'}
        item['in_office'] = True
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        item['constituency'] = response.request.meta['constituency']

        img_url = sel.xpath(".//td[@bgcolor='B8DD6C']/img/@src").extract()[0]
        print img_url
        item['image'] = urljoin(response.url, urllib.quote(img_url.encode('utf8')))
        print item['image']

        details = sel.xpath(".//th[@class='T84 color06']/..")
        print len(details)
        item['contact_details']=[]
        for detail in details:
            info = detail.xpath(".//th/text()")
            content = re.sub('\s', '', detail.xpath(".//td/span/text()").extract()[0])
            if info.re(u'[\s]*黨[\s]*籍[\s]*'):
                item['party'] = content
                print item['party']
            if info.re(u'[\s]*選[\s]*區[\s]*'):
                item['district'] = content
                print item['district']
            if info.re(u'[\s]*地[\s]*址[\s]*'):
                print content
                item['contact_details'].append({'type': 'address', 'label': u'通訊處', 'value': content})
            if info.re(u'[\s]*電[\s]*話[\s]*'):
                print content
                item['contact_details'].append({'type': 'voice', 'label': u'電話', 'value': content})
            if info.re(u'[\s]*傳[\s]*真[\s]*'):
                print content
                item['contact_details'].append({'type': 'fax', 'label': u'傳真', 'value': content})
            if info.re(u'[\s]*學[\s]*歷[\s]*'):
                item['education'] = [x.strip() for x in detail.xpath(".//td/span/text()").extract()]
                print item['education']
            if info.re(u'[\s]*經[\s]*歷[\s]*'):
                item['experience'] = [x.strip() for x in detail.xpath(".//td/span/text()").extract()]
                print item['experience']
        return item
