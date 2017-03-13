#-*- coding: utf-8 -*-
import re
import os
import json
import urllib
from urlparse import urljoin
import scrapy

class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.cyscc.gov.tw"]
    start_urls = ["http://www.cyscc.gov.tw/chinese/Parliamentary_index.aspx?n=29"]

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'constituency.json'), 'r') as infile:
            self.constituency = json.loads(infile.read())
        with open(os.path.join(os.path.dirname(__file__), '../../data/cand-moi-county-control-2018.json'), 'r') as infile:
            self.ref = {re.sub(u'[\s　]', '', person['idname']): person for person in json.loads(infile.read()) if person['cityname'] == u'嘉義縣'}


    def parse(self, response):
        for node in response.xpath(u'//a/img[re:test(@alt, "議員$")]'):
            item = {}
            item['image'] = urljoin(response.url, node.xpath("@src").extract_first())
            img_alt = node.xpath('@alt').extract_first().strip(u'議員')
            m = re.search(u'(?P<first_name>[^\(\s]+)\s*(?P<title>[^\(\s]+)?\s*(?P<last_name>[^\(\s]*)(?P<remark>\(\S+\))?', img_alt)
            item['remark'] = m.group('remark') if m.group('remark') else ''
            item['in_office'] = False if m.group('remark') else True
            item['name'] = m.group('first_name') + m.group('last_name')
            item['title'] = m.group('title') if m.group('title') else u'議員'
            yield scrapy.Request(urljoin(response.url, node.xpath('parent::a/@href').extract_first()), callback=self.parse_profile, meta={'item': item})

    def parse_profile(self, response):
        item = response.meta['item']
        item['county'] = u'嘉義縣'
        item['election_year'] = '2014'
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': '2018-12-25'}
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        item['constituency'] = response.xpath("//*[@id='ctl00_ContentPlaceHolder1_fvDetail_Label3']/text()").re(u'第\S+選區')[0]
        item['district'] = self.constituency[item['constituency']]
        item['gender'] = response.xpath("//*[@id='ctl00_ContentPlaceHolder1_fvDetail_Label6']/text()").extract_first()
        item['contact_details'] = []
        for id, label, name in [('Tel', u'電話', 'voice'), ('Address', u'通訊處', 'address') , ('Email', u'電子信箱', 'email')]:
            value = response.xpath('//tr[@id="ctl00_ContentPlaceHolder1_fvDetail_tr_%s"]/td[@class="emword"]/text()' % id).extract_first().strip()
            if value:
                item['contact_details'].append({'type': name, 'label': label, 'value': value})
        item['education'] = [x.strip() for x in response.xpath(u'//span[@class="word_redblod" and re:test(., "學歷：")]/following-sibling::span[1]/text()').extract() if x.strip()]
        item['experience'] = [x.strip() for x in response.xpath(u'//span[@class="word_redblod" and re:test(., "經歷：")]/following-sibling::span[1]/text()').extract() if x.strip()]
        item['platform'] = [x.strip() for x in response.xpath(u'//span[@class="word_redblod" and re:test(., "政見：")]/following-sibling::span[1]/text()').extract() if x.strip()]
        item['party'] = self.ref.get(item['name'], {}).get('partymship', '')
        yield item
