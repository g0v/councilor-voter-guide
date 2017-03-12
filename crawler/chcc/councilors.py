#-*- coding: utf-8 -*-
import os
import re
import json
import urllib
from urlparse import urljoin
import scrapy


def GetDate(text):
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
    start_urls = ["http://www.chcc.gov.tw/member/index.aspx?Parser=99,6,40"]
    download_delay = 0.5

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), '../../data/cand-moi-county-control-2018.json'), 'r') as infile:
            self.ref = {re.sub(u'[\s　]', '', person['idname']): person for person in json.loads(infile.read()) if person['cityname'] == u'彰化縣'}

    def parse(self, response):
        nodes = response.xpath(u'//a[re:test(., "^第\S+選區：")]')
        for node in nodes:
            constituency, district = node.xpath('text()').extract_first().split(u'：')
            for person in node.xpath('parent::dt/following-sibling::dd/descendant::a[1]'):
                item = {}
                item['constituency'] = constituency
                item['district'] = district
                item['name'] = person.xpath('text()').extract_first()
                yield scrapy.Request(urljoin(response.url, person.xpath('@href').extract_first()), callback=self.parse_profile, meta={'item': item})

    def parse_profile(self, response):
        item = response.meta['item']
        item['county'] = u'彰化縣'
        item['election_year'] = '2014'
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': '2018-12-25'}
        item['in_office'] = True
        image = response.xpath('//img[@alt="%s"]/@src' % item['name']).extract_first()
        item['image'] = urljoin(response.url, urllib.quote(image.encode(response.encoding)))
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        fb = response.xpath('//img[re:test(@alt, "%s\s*Facebook")]/ancestor::a[1]/@href' % item['name']).extract_first()
        if fb:
            item['links'].append({'url': fb, 'note': u'個人臉書'})
        item['gender'] = response.xpath(u'//span[re:test(., "性別：")]/parent::div/text()').extract_first().strip()
        item['party'] = response.xpath(u'//span[re:test(., "政黨：")]/parent::div/text()').extract_first().strip()
        item['birth'] = GetDate(re.sub(u'[\s　]', '', response.xpath(u'//span[re:test(., "生日：")]/parent::div/text()').extract_first()))
        item['title'] = response.xpath(u'//span[re:test(., "現任：")]/parent::div/text()').re(u'(議長|副議長|議員)')[0].strip()
        item['contact_details'] = []
        contact_mappings = {
            u'電話': 'voice',
            u'行動': 'cell',
            u'傳真': 'fax',
            u'地址': 'address'
        }
        for label, name in contact_mappings.items():
            values = [x.strip() for x in response.xpath(u'//span[re:test(., "%s：")]/parent::div/text()' % label).extract() if x.strip()]
            for value in values:
                item['contact_details'].append({
                    'label': label,
                    'type': name,
                    'value': value
                })
        values = [x.strip('mailto://') for x in response.xpath(u'//span[re:test(., "電子信箱：")]/parent::div/a/@href').extract() if x.strip('mailto://')]
        for value in values:
            item['contact_details'].append({
                'label':  u'電子信箱',
                'type': 'email',
                'value': value
            })
        item['education'] = [x.strip() for x in response.xpath(u'//div[@class="member_title_u member_title3"]/text()').extract() if x.strip()]
        item['experience'] = [x.strip() for x in response.xpath(u'//div[@class="member_title_u member_title4"]/text()').extract() if x.strip()]
        yield scrapy.Request(urljoin(response.url, response.xpath(u'//a[@title="政見"]/@href').extract_first()), callback=self.parse_platform, meta={'item': item})

    def parse_platform(self, response):
        item = response.meta['item']
        item['platform'] = []
        for x in response.xpath(u'//table[@class="bt_table_line"]/descendant::tr'):
            line = re.sub('\s', '', x.xpath('string()').extract_first())
            if line:
                item['platform'].append(line)
        yield item
