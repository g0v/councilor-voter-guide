#-*- coding: utf-8 -*-
import re
import scrapy
from scrapy.selector import Selector
from chcc.items import Councilor
import urllib
from urlparse import urljoin
from scrapy.http import Request

def ROC2AD(text):
    matchTerm = re.search(u'''
        (?P<year>[\d]+)[\s]*(年|[./-])[\s]*
        (?P<month>[\d]+)[\s]*(月|[./-])[\s]*
        (?P<day>[\d]+)
    ''', text, re.X)
    if matchTerm:
        return '%04d-%02d-%02d' % (int(matchTerm.group('year'))+1911, int(matchTerm.group('month')), int(matchTerm.group('day')))
    else:
        return None

class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.chcc.gov.tw"]
    start_urls = [
        "http://www.chcc.gov.tw/content/list/list01-map.aspx"
    ]
    download_delay = 0.5

    def parse(self, response):
        nodes = response.xpath('//table/tr/td/a[contains(@href, "list01.aspx?EType")]')
        for node in nodes:
            constituency, district = node.xpath('text()').extract()[0].split(u'：')
            for link in node.xpath('../../td[2]//a/@href').extract():
                item = Councilor()
                item['constituency'] = constituency
                item['district'] = district
                yield Request(urljoin(self.start_urls[0], link), callback=self.parse_profile, meta={'item': item})

    def parse_profile(self, response):
        '''
        filename = 'test'
        with open(filename, 'wb') as f:
            f.write(response.body)
        '''
        print response
        sel = Selector(response)
        item = response.meta['item']
        image = sel.xpath('//table/tr/td/img/@src').extract()[0]
        item['image'] = urljoin(response.url, urllib.quote(image.encode('utf8')))
        print item['image']
        #第七選區議員 謝典霖
        text = sel.xpath('//table/tr/td/img/@alt').extract()[0].encode('utf8')
        strings = text.split(' ')
        idx = strings[0].find('議員')
        print item['constituency']
        item['name'] = strings[1]
        detail = sel.xpath('//table')
        nodes = detail[6].xpath('tr')
        item['county'] = '彰化縣'
        item['election_year'] = '2009'
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': '2014-12-25'}
        item['title'] = sel.xpath('//span[@class="orange01"]/text()').extract()[0].split()[0]
        item['in_office'] = True
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        item['contact_details'] = []
        item['experience'] = []
        for node in nodes:
            if node.xpath('td/text()').re(u'性[\s]*別'):
                obj= node.xpath('td/text()').extract()
                if len(obj)==2:
                    item['gender']=obj[1]
            if node.xpath('td/text()').re(u'生[\s]*日'):
                obj= node.xpath('td/text()').extract()
                if len(obj)==2:
                    item['birth']=ROC2AD(obj[1])
                #print item['birth'].encode('utf8')
            if node.xpath('td/text()').re(u'電[\s]*話'):
                obj= node.xpath('td/text()').extract()
                phone=''
                if len(obj)==2:
                    phone = obj[1]
                item['contact_details'].append({'type': 'phone', 'label': u'電話', 'value': phone})
            if node.xpath('td/text()').re(u'傳[\s]*真'):
                obj= node.xpath('td/text()').extract()
                fax=''
                if len(obj)==2:
                    fax = obj[1]
                item['contact_details'].append({'type': 'fax', 'label': u'傳真', 'value': fax})
                #print fax
            if node.xpath('td/text()').re('E-mail[\s]*'):
                obj= node.xpath('td/text()').extract()
                email=''
                if len(obj)==2:
                    email = obj[1]
                item['contact_details'].append({'type': 'email', 'label': u'電子信箱', 'value': email})
                print email
            if node.xpath('td/text()').re(u'地[\s]*址'):
                obj= node.xpath('td/text()').extract()
                address=''
                if len(obj)==2:
                    address = obj[1]
                item['contact_details'].append({'type': 'address', 'label': u'通訊處', 'value': address})
                print address.encode('utf8')
            if node.xpath('td/text()').re(u'學[\s]*歷'):
                obj= node.xpath('td/text()').extract()
                if len(obj)==2:
                    item['education'] = obj[1]
            if node.xpath('td/text()').re(u'經[\s]*歷'):
                for obj in node.xpath('td/text()').extract()[1:]:
                    print obj.encode('utf8')
                    item['experience'].append(obj)
            if node.xpath('td/text()').re(u'現[\s]*任'):
                for obj in node.xpath('td/text()').extract()[1:]:
                    print obj.encode('utf8')
                    item['experience'].append(obj)
        platforms=detail[2].xpath('tr')
        print detail[2].extract().encode('utf8')
        item['platform']=[]
        for platform in platforms:
            obj=platform.xpath('td/text()').extract()[0]
            obj=obj.replace('\r\n','').replace(' ','')
            print obj
            if len(obj):
                item['platform'].append(obj)
        return item
