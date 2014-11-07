# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.selector import Selector
from ylcc.items import Councilor
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
         "http://localhost/y1.html"
    ]
    '''
    allowed_domains = ["www.ylcc.gov.tw"]
    start_urls = [
         "http://www.ylcc.gov.tw/index.php?"
    ]
    
    def __init__(self):
        fh=open(os.path.join(os.path.dirname(__file__), 'constituency.json'), 'r')
        self.constituency = json.loads(fh.read())

    def parse(self, response):  
        result=[]
        patterns=['y6']

        for idx in range(1,7):
            url='http://www.ylcc.gov.tw/index.php?inner=member_precinct'+ str(idx) 
            print url
            profile = Request(url, callback=self.parse_profile)
            result.append(profile)
        return result          
        '''
        for pattern in patterns:
            url='http://localhost/'+ pattern + '.html'
            print url
            profile = Request(url, callback=self.parse_profile)
            result.append(profile)
        return result
        '''

    def parse_profile(self, response):
        district=int(response.url[-1])
        #tail=response.url.split("/")[-1]
        #district=int(tail[1:2])
        print district

        sel = Selector(response)  
        photourls=sel.xpath(".//td[@class='bg_member_1']")
        #print len(photourls)
        photolink={}
        for obj in photourls:
            image=obj.xpath('.//following-sibling::node()/img/@src').extract()[0].encode('utf8')
            imagename=obj.xpath('.//following-sibling::node()/img/@alt').extract()[0].encode('utf8')
            #print imagename
            photourl = urljoin(response.url, urllib.quote(image))
            photolink [imagename]=photourl
        #print photolink
        itemresult=[]
        candidates = sel.xpath(".//span[@class='word_orange']/..")
        print len(candidates)
        for candidate in candidates:
            print candidate.extract().encode('utf8')
            item = Councilor() 
            names = candidate.xpath(".//span[@class='word_orange']/text()").extract()
            if len(names):
                item['name']=names[0].encode('utf8')
                print item['name']
                photoname=item['name']+'照片'
                if photolink.has_key(photoname):
                    item['image']=photolink[photoname]
                item['election_year']='2009'
                item['county']='雲林縣'
                item['district']=self.constituency[str(district)]
                place=u'第'+unicode(district)+u'選區'
                item['constituency']=place
                #print item['constituency']

                item['contact_details']=[]

                details=candidate.xpath(".//node()[preceding-sibling::br][not(self::br)]")
                for idx in range(len(details)):
                    if details[idx].re(u'[\s]*學[\s]*歷[\s]*'):
                        obj=details[idx+1].extract().encode('utf8').replace('\n','').replace(' ','').replace('\r','')
                        item['education']=obj
                        #print 'education=',item['education']
                    if details[idx].re(u'[\s]*經[\s]*歷[\s]*'):
                        obj=details[idx+1].extract().encode('utf8').replace('\n','').replace(' ','').replace('\r','')
                        item['experience']=obj
                        #print 'experience=',item['experience']
                    if details[idx].re(u'[\s]*黨[\s]*籍[\s]*'):
                        obj=details[idx+1].extract().encode('utf8').replace('\n','').replace(' ','').replace('\r','')
                        item['party']=obj
                        #print 'party=',item['party']
                    if details[idx].re(u'[\s]*服[\s]*務[\s]*處[\s]*電[\s]*話[\s]*'):
                        phone=details[idx+1].extract().encode('utf8').replace('\n','').replace(' ','')\
                        .replace('\r','').replace('\t','')
                        item['contact_details'].append({'type': 'voice', 'label': u'電話', 'value': phone})
                    if details[idx].re(u'[\s]*服[\s]*務[\s]*處[\s]*傳[\s]*真[\s]*'):
                        fax=details[idx+1].extract().encode('utf8').replace('\n','').replace(' ','')\
                        .replace('\r','').replace('\t','')
                        item['contact_details'].append({'type': 'voice', 'label': u'傳真', 'value': fax})
                    if details[idx].re(u'[\s]*服[\s]*務[\s]*處[\s]*地[\s]*址[\s]*'):
                        address=details[idx+1].extract().encode('utf8').replace('\n','').replace(' ','')\
                        .replace('\r','').replace('\t','')
                        item['contact_details'].append({'type': 'voice', 'label': u'通訊處', 'value': address})
                    if details[idx].re(u'[\s]*電[\s]*子[\s]*信[\s]*箱[\s]*'):
                        email=details[idx+1].extract().encode('utf8').replace('\n','').replace(' ','')\
                        .replace('\r','').replace('\t','')
                        item['contact_details'].append({'type': 'voice', 'label': u'電子信箱', 'value': email})
            itemresult.append(item)

        return itemresult
        
        