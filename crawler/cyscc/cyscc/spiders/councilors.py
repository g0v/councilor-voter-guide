#-*- coding: utf-8 -*-
import re
import os
import json
import urllib
from urlparse import urljoin
import scrapy
from scrapy.selector import Selector
from cyscc.items import Councilor
from scrapy.http import Request

class Spider(scrapy.Spider):
    name = "councilors"

    allowed_domains = ["www.cyscc.gov.tw"]
    start_urls = [
         "http://www.cyscc.gov.tw/chinese/Parliamentary_index.aspx?n=29"
    ]
    '''
    allowed_domains = ["localhost"]
    start_urls = [
         "http://localhost/1.html"
    ]
    '''
    def __init__(self):
        fh=open(os.path.join(os.path.dirname(__file__), 'constituency.json'), 'r')
        self.constituency = json.loads(fh.read())


    def parse(self, response):
        for link in response.xpath('//a[contains(@href, "chinese/Parliamentary_Detail.aspx")]'):
            image = urljoin("http://www.cyscc.gov.tw", link.xpath("img/@src").extract()[0])
            yield Request(urljoin("http://www.cyscc.gov.tw", link.xpath('@href').extract()[0]), callback=self.parse_profile, meta={"image": image})


    def parse_profile(self, response):
    	sel = Selector(response)
        item = Councilor()
        obj=sel.xpath("//span[@id='ctl00_ContentPlaceHolder1_fvDetail_Label3']/text()")
        item['county']='嘉義縣'
        item['election_year']='2009'
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': '2014-12-25'}
        item['in_office'] = True
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        item["image"] = response.request.meta["image"]
        item['contact_details']=[]
        item['experience']=[]
        item['platform']=[]
        item['education']=[]
        if len(obj):
            item['constituency']=obj[0].extract().encode('utf8')
            print item['constituency']
            item['district']=self.constituency[obj[0].extract()]
            print item['district']

        obj=sel.xpath("//span[@id='ctl00_ContentPlaceHolder1_fvDetail_Label6']/text()")
        if len(obj):
            item['gender']=obj[0].extract().encode('utf8')
            #print item['gender']

        obj=sel.xpath("//tr[@id='ctl00_ContentPlaceHolder1_fvDetail_tr_Tel']/td[2]/text()")
        if len(obj):
            phone=obj[0].extract().encode('utf8').replace(' ','').replace('\r\n','').replace('\n','')
            item['contact_details'].append({'type': 'phone', 'label': u'電話', 'value': phone})

        obj=sel.xpath("//tr[@id='ctl00_ContentPlaceHolder1_fvDetail_tr_Address']/td[2]/text()")
        if len(obj):
            address=obj[0].extract().encode('utf8').replace(' ','').replace('\r\n','').replace('\n','')
            item['contact_details'].append({'type': 'address', 'label': u'通訊處', 'value': address})

        obj=sel.xpath("//tr[@id='ctl00_ContentPlaceHolder1_fvDetail_tr_Email']/td[2]/text()")
        if len(obj):
            email=obj[0].extract().encode('utf8').replace(' ','').replace('\r\n','').replace('\n','')
            item['contact_details'].append({'type': 'email', 'label': u'電子信箱', 'value': email})

        schools=sel.xpath("//tr[@id='ctl00_ContentPlaceHolder1_fvDetail_tr_Content_1']/td[1]/span[2]/text()")
        print len(obj)
        if len(obj):
            for obj in schools:
                school=obj.extract().encode('utf8').replace(' ','').replace('\n','').replace('\r','')
                item['education'].append(school)
        print item['education']

        experiences=sel.xpath("//tr[@id='ctl00_ContentPlaceHolder1_fvDetail_tr_Content_2']/td/span[2]/text()")
        #print len(experiences)
        if len(experiences):
            for obj in experiences:
                experience=obj.extract().encode('utf8').replace(' ','').replace('\r','').replace('\t','')
                #print experience
                item['experience'].append(experience)

        platforms=sel.xpath("//tr[@id='ctl00_ContentPlaceHolder1_fvDetail_tr_Content_3']/td/span[2]/text()")
        #print len(platforms)
        if len(platforms):
            for obj in platforms:
                platform=obj.extract().encode('utf8').replace(' ','').replace('\r','').replace('\n','')
                #print platform
                item['platform'].append(platform)

        names=sel.xpath("//td[@class='name']/text()")
        #print len(names)
        if len(names):
            obj=names[2].extract().replace(' ','').replace('\r','').replace('\r\n','').replace('\n','')
            print len(obj)
            idx=obj.find('(')
            item['name']=obj[0:idx-1]
            print item['name']

        return item
