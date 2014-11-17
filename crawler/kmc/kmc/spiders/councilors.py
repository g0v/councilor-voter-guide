# -*- coding: utf-8 -*-
import re
import urllib
from urlparse import urljoin
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from kmc.items import Councilor
import requests
import json

## 用開放資料比對議員性別
url = "http://cand.moi.gov.tw/of/ap/cand_json.jsp?electkind=0200000"
r = requests.get(url)
namejson = json.loads(r.content.strip(' \s\n\r'))
def GetGender(json,name):
    for i in json:
        s = re.sub(u'[\s　]', '', i['idname'])
        if(s==name):
            return i['sex']

## 轉換年月日格式
def GetDate(text):
    matchTerm = re.search(u'''
        (?P<year>[\d]+)[\s]*年[\s]*
        (?P<month>[\d]+)[\s]*月[\s]*
        (?P<day>[\d]+)
    ''', text, re.X)
    if matchTerm:
        return '%04d-%02d-%02d' % (int(matchTerm.group('year'))+1911, int(matchTerm.group('month')), int(matchTerm.group('day')))
    else:
        return None

class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.kmc.gov.tw/"]
    start_urls = ["http://www.kmc.gov.tw/KMCII/coun_info_1.aspx",]
    download_delay = 0.5


    def parse(self, response):
        sel = Selector(response)
        #nodes = sel.xpath('//table//tr/td/a[contains(@href, "coun_info_1.aspx")]/@href') # for TEST
        nodes = sel.xpath('//table//tr/td/a[contains(@href, "coun_info")]/@href') # Get 所有候選人連結
        for node in nodes:
            yield Request('http://%s%s' % ("www.kmc.gov.tw/KMCII/", node.extract()), callback=self.parse_profile, dont_filter=True)

    def parse_profile(self, response):
        global namejson
        sel = Selector(response)
        item = Councilor()
        name = sel.xpath("//table/tr/td/a[@href='%s']/text()" % re.search("\w+.\w+$",response.url).group()).extract()[0]
        education = sel.xpath('//table/tr[1]/td/table/tr/td[2]/table/tr/td[2]//table/tr[2]/td/text()').extract()
        item['education'] = [x.strip(' \s\t\n\r') for x in education] # 學歷
        email = sel.xpath('//table/tr[8]/td[3]/a/text()').extract()
        phone = sel.xpath('//table/tr[6]/td[3]/text()').extract()
        fax = sel.xpath('//table/tr[7]/td[3]/text()').extract()
        address = sel.xpath('//table/tr[5]/td[3]/text()').extract()
        item['contact_details'] = []
        if email:
            item['contact_details'].append({'type': 'email', 'label': u'電子信箱', 'value': email[0].strip()}) # email
        if phone:
            item['contact_details'].append({'type': 'voice', 'label': u'電話', 'value': phone[0].strip()}) # 電話
        if fax:
            item['contact_details'].append({'type': 'fax', 'label': u'傳真', 'value': fax[0].strip()}) # 傳真
        if address:
            item['contact_details'].append({'type': 'address', 'label': u'通訊處', 'value': address[0].strip()}) # 服務處
	page = re.search("\w+.\w+$",response.url).group()
	pageNum = re.search("[0-9]+",page).group()
	if (int(pageNum) < 17):
            districtXpath = "//table/tr/td/a[@href='%s']/../../td[1]/text()" % page
	else:
            districtXpath = "//table/tr/td/a[@href='%s']/../../td[7]/text()" % page
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        item['district'] = sel.xpath("//table/tr/td/a[@href='%s']/../../td[1]/text()" % re.search("\w+.\w+$",response.url).group()).extract()[0] # 行政區
        item['gender'] = GetGender(namejson,name) # 性別 : 網頁上沒有標性別....使用開放資料比對議員性別
        item['image'] = "http://www.kmc.gov.tw/kmcii/" + sel.xpath('//img[1]/@src').extract()[0]
        experience = sel.xpath('//table/tr[1]/td/table/tr/td[2]/table/tr/td[2]//table/tr[3]/td/text()').extract()
        item['experience'] = [x.strip() for x in experience] # 經歷
        item['county'] = u'基隆市'
        platform = sel.xpath("//table/tr[2]/td/table[2]/tr/td/table/tr[2]/td/table[1]/tr[2]/descendant::*/text()").extract()
        item['platform'] = [x.strip() for x in platform] #政見
        item['birth'] = GetDate(sel.xpath('//table/tr[4]/td[3]/text()').extract()[0]) # 出生日
        item['in_office'] = True # 是否還在職
        item['party'] = sel.xpath('//table/tr[3]/td[3]/text()').extract()[0] # 黨籍
        item['constituency'] = sel.xpath('//table/tr[2]/td[3]/text()').extract()[0] # 第 N 選區
        item['election_year'] = '2009' # 選舉年度
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': '2014-12-25'}
        item['name'] = name # 姓名
        return item
