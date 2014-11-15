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
    
    def __init__(self):
        fh=open(os.path.join(os.path.dirname(__file__), 'constituency.json'), 'r')
        self.constituency = json.loads(fh.read())

    def parse(self, response):
        result=[]
        sel= Selector(response)
        index_table=sel.xpath(".//td[@class='list borderleft']")
        candidates=index_table.xpath(".//a/@href")
        for candidate in candidates:
            url=urljoin(response.url, candidate.extract())
            print url
            profile = Request(url, callback=self.parse_profile)
            result.append(profile)
        return result        
            

    def parse_profile(self, response):
        sel = Selector(response) 
        item = Councilor()

        item['election_year']='2009'
        item['county']='屏東縣'
        img_url=sel.xpath(".//td[@bgcolor='#E8E8E8']/img/@src").extract()[0]
        item['image'] = urljoin(response.url, img_url)
        print item['image']

        name_parent=sel.xpath(".//td[@bgcolor='#E8E8E8']/../..")
        name=name_parent.xpath(".//tr/td/text()").extract()[0].replace(u'議員：','')
        item['name']=name
        print item['name']

        item['contact_details']=[]
        item['platform']=[]
        details=sel.xpath(".//td[@class='list']/..") 
        for detail in details:
            info=detail.xpath(".//td/text()")
            if info[0].re(u'[\s]*黨[\s]*籍[\s]*'):
                item['party']=info[1].extract()
                print item['party']
            if info[0].re(u'[\s]*選[\s]*區[\s]*'):
                obj=info[1].extract()
                district_key=obj[:-1]
                item['district']=self.constituency[district_key]
                item['constituency']=obj
            if info[0].re(u'[\s]*性[\s]*別[\s]*'):
                item['gender']=info[1].extract()    
            if info[0].re(u'[\s]*聯[\s]*絡[\s]*處[\s]*'):
                address=info[1].extract() 
                item['contact_details'].append({'type': 'voice', 'label': u'通訊處', 'value': address})
            if info[0].re(u'[\s]*電[\s]*話[\s]*'):
                phone=info[1].extract()
                item['contact_details'].append({'type': 'voice', 'label': u'電話', 'value': phone})        
            if info[0].re(u'[\s]*傳[\s]*真[\s]*'):
                fax=info[1].extract()
                item['contact_details'].append({'type': 'voice', 'label': u'傳真', 'value': fax})        
            if info[0].re(u'[\s]*電[\s]*子[\s]*郵[\s]*件[\s]*'):
                email=info[1].extract()
                item['contact_details'].append({'type': 'voice', 'label': u'電子信箱', 'value': email})        
            if info[0].re(u'[\s]*簡[\s]*介[\s]*'):    
                for idx in range(1,len(info)):
                    #print info[idx].extract()
                    item['platform'].append(info[idx].extract().replace('\r\n',''))
        return item            
    
    

