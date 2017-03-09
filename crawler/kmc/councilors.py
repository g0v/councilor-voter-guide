# -*- coding: utf-8 -*-
import re
import urllib
from urlparse import urljoin
import scrapy
import requests
import json

## 用開放資料比對議員性別
r = requests.get("http://cand.moi.gov.tw/of/ap/cand_json.jsp?electkind=0200000")
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
    allowed_domains = ["www.kmc.gov.tw"]
    start_urls = ["http://www.kmc.gov.tw/index.php/kmc-info/%E8%AD%B0%E5%93%A1%E8%B3%87%E8%A8%8A",]
    download_delay = 0.5

    def parse(self, response):
        nodes = response.xpath(u'//a[re:test(@title, "議(員|長)$")]')
        for node in nodes:
            item = {}
            item['election_year'] = '2014'
            item['in_office'] = True
            item['term_start'] = '%s-12-25' % item['election_year']
            item['term_end'] = {'date': '2018-12-24'}
            item['name'], item['title'] = node.xpath('@title').extract_first().split()
            item['gender'] = GetGender(namejson, item['name'])
            item['county'] = u'基隆市'
            item['district'] = node.xpath('normalize-space(string(ancestor::tr/td[1]))').extract_first()
            yield scrapy.Request(urljoin(response.url, node.xpath('@href').extract_first()), callback=self.parse_profile, meta={'item': item})

    def parse_profile(self, response):
        global namejson
        item = response.meta['item']
        item['image'] = response.xpath('//img[contains(@src, "/member/")]/@src').extract_first()
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        item['constituency'] = response.xpath('//td/text()').re(u'選區：\s*(.+)')[0].strip()
        item['party'] = response.xpath('//td/text()').re(u'政黨：\s*(.+)')[0].strip()
        item['birth'] = GetDate(response.xpath('//td/text()').re(u'出生日期：\s*(.+)')[0]).strip()
        website = response.xpath('//td/text()').re(u'網站連結：\s*(.+)')
        if website:
            item['links'].append({'url': website[0].strip(), 'note': u'個人網站'})
        item['contact_details'] = []
        contact_mappings = {
            u'連絡電話': 'voice',
            u'傳真號碼': 'fax',
            u'服務處': 'address',
            u'電子郵件': 'email'
        }
        for label, name in contact_mappings.items():
            values = [x.strip() for x in response.xpath(u'//td[re:test(., "%s：")]/text()' % '\s*'.join(label)).re(u'%s：\s*(.+)\s*' % label) if x.strip()]
            for value in values:
                item['contact_details'].append({
                    'label': label,
                    'type': name,
                    'value': value
                })
        item['experience'] = [x.strip() for x in response.xpath(u'//img[contains(@src, "speaker0")]')[1].xpath('ancestor::tr/following-sibling::tr[1]//tr/td[1]/text()').extract() if x.strip()]
        item['platform'] = [x.strip() for x in response.xpath(u'//img[contains(@src, "speaker0")]')[2].xpath('ancestor::tr/following-sibling::tr[1]//tr/td[1]/text()').extract() if x.strip()]
        yield item
