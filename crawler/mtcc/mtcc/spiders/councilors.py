# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.selector import Selector
from mtcc.items import Councilor
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
         "http://localhost/m7.html"
    ]
    '''
    allowed_domains = ["www.mtcc.gov.tw"]
    start_urls = [
         "http://www.mtcc.gov.tw/"
    ]
    download_delay = 0.5

    def __init__(self):
        #fh=open(os.path.join(os.path.dirname(__file__), 'constituency.json'), 'r')
        #self.constituency = json.loads(fh.read())
        pass

    def parse(self, response):
        result = []
        patterns = ['http://www.mtcc.gov.tw/ab_speaker.htm','http://www.mtcc.gov.tw/ab_speaker2.htm']

        for pattern in patterns:
            print pattern
            profile = Request(pattern, callback=self.parse_profile)
            result.append(profile)

        for idx in range(1, 8):
            url = 'http://www.mtcc.gov.tw/cu_representative%d.htm' % idx
            profile = Request(url, callback=self.parse_profile)
            result.append(profile)

        return result

    def parse_profile(self, response):
        sel = Selector(response)
        item = Councilor()

        item['election_year'] = '2009'
        item['county'] = u'連江縣'
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': '2014-12-25'}
        item['in_office'] = True
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]

        name = sel.xpath(".//td[@class='text15w']/text()").extract()[0][-3:]
        item['name'] = name
        print item['name']

        img_parent = sel.xpath(".//td[@style='background-image: url(images/table_1.gif);']/../../../../..")
        img_url = img_parent.xpath(".//td/img/@src").extract()[0]
        #print img_url
        item['image'] = urljoin(response.url, img_url)
        print item['image']
        details = sel.xpath(".//td[@style='background-image: url(images/table_2.gif);']/table/tr")
        print len(details)
        if not len(details):
            details = sel.xpath(".//td[@style='background-image: url(images/table_2.gif);']/table/tbody/tr")
        item['contact_details'] = []
        item['experience'] = []
        item['platform'] = []
        for detail in details:
            info = detail.xpath(".//th")
            if not len(info):
                info = detail.xpath(".//th/span")
                #print 'another info',len(info)
            if not len(info):
                info = detail.xpath(".//th/p")
            if not len(info):
                #print 'next run'
                continue

            print info[0].xpath(".//text()").extract()[0]

            content_parent = detail.xpath(".//td")
            content = content_parent.xpath(".//text()")
            if not len(content):
                content = detail.xpath(".//span/text()")
                #print 'another content',len(content)
            obj = ''
            if len(content) == 2:
                obj = content[1].extract()
                #print content[1].extract()
            if len(content) == 1:
                obj = content[0].extract()
                #print content[0].extract()
            if info[0].re(u'[\s]*性[\s]*別[\s]*'):
                item['gender'] = obj
#           if info[0].re(u'[\s]*年[\s]*齡[\s]*'):
#               item['birth'] = obj
#               print item['birth']
            if info[0].re(u'[\s]*黨[\s]*籍[\s]*'):
                item['party'] = obj
            if info[0].re(u'[\s]*選[\s]*區[\s]*'):
                m = re.search(u'(?P<constituency>\S*?)\s*[(（](?P<district>\S*)[)）]', obj)
                item['constituency'] = m.group('constituency')
                item['district'] = m.group('district')
                print item['district']
            if info[0].re(u'[\s]*服[\s]*務[\s]*處[\s]*地[\s]*址[\s]*'):
                item['contact_details'].append({'type': 'address', 'label': u'通訊處', 'value': obj})
            if info[0].re(u'[\s]*服[\s]*務[\s]*處[\s]*電[\s]*話[\s]*'):
                item['contact_details'].append({'type': 'voice', 'label': u'電話', 'value': obj})
            if info[0].re(u'[\s]*簡[\s]*經[\s]*歷[\s]*'):
                item['experience'] = [x.strip() for x in detail.xpath(".//td/p/text()").extract()]
            if info[0].re(u'[\s]*政[\s]*見[\s]*'):
                platform_parent = detail.xpath(".//td")
                if len(platform_parent) > 1:
                    platforms = platform_parent[1].xpath(".//p/text()")
                    print '1 type=', len(platforms)
                    if len(platforms):
                        item['platform'] = [x.strip() for x in platforms.extract()]
                    else:
                        platforms = platform_parent[1].xpath(".//table/tbody/tr")
                        print '2 type=', len(platforms)
                        platforms = platform_parent[1].xpath(".//table/tr")
                        print '3 type=', len(platforms)
                        if len(platforms):
                            for platform in platforms:
                                texts = platform.xpath(".//td/span")
                                if len(texts) > 1:
                                    obj = texts[1].xpath("..//text()").extract()[0].replace('\r\n','')
                                    item['platform'].append(obj)
        return item
