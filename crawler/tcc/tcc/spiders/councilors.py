# -*- coding: utf-8 -*-
import re
import urllib
from urlparse import urljoin
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from tcc.items import Councilor


def take_first(list_in):
    if len(list_in) == 1:
        return list_in[0]
    else:
        return ''

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
    allowed_domains = ["www.tcc.gov.tw"]
    start_urls = ["http://www.tcc.gov.tw/Councilor_Main.aspx",]
    download_delay = 0.5

    def parse(self, response):
        sel = Selector(response)
        nodes = sel.xpath('//table/tr/td/a[contains(@href, "Councilor_Content.aspx")]')
        for node in nodes:
            yield Request('http://%s%s' % ("www.tcc.gov.tw/", take_first(node.xpath('@href').extract())), callback=self.parse_profile)

    def parse_profile(self, response):
        sel = Selector(response)
        item = Councilor()
        image = sel.xpath('//table/tr/td/div[@class="aldermans_photo"]/img/@src').extract()[0]
        item['image'] = urljoin(response.url, urllib.quote(image.encode('utf8')))
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        constituency = take_first(sel.xpath('//div/h3/span[@id="FormView1_ElectionZoneLabel"]/text()').extract())
        match = re.search(u'''
            第[\W]{1,3}屆
            (?P<county>[\W]{1,3}(?:縣|市))議員
            [\s]/[\s]
            (?P<selection>第[\W]{1,3}選區)
            [\s]
            （(?P<district>[\S]*)）
        ''', constituency, re.X)
        if match:
            item['constituency'] = '%s%s' % (match.group('county'), match.group('selection'))
            item['county'] = match.group('county')
            item['district'] = match.group('district')
        nodes = sel.xpath('//table[@class="aldermans_information"]/tr')
        item['contact_details'] = []
        for node in nodes:
            if node.xpath('td/text()').re(u'姓[\s]*名'):
                item['name'] = re.sub(u'\s|　', '', node.xpath('td/span/text()').extract()[0])
            if node.xpath('td/text()').re(u'性[\s]*別'):
                item['gender'] = take_first(node.xpath('td/span/text()').re(u'[\s]*([\S]+)[\s]*'))
            if node.xpath('td/text()').re(u'出[\s]*生'):
                item['birth'] = GetDate(take_first(node.xpath('td/span/text()').extract()))
            if node.xpath('td/text()').re(u'黨[\s]*籍'):
                item['party'] = take_first(node.xpath('td/span/text()').re(u'[\s]*([\S]+)[\s]*'))
            if node.xpath('td/text()').re(u'個人網站'):
                for link in node.xpath('td/a/@href').re(u'[\s]*([\S]+)[\s]*'):
                    item['links'].append({'url': link, 'note': u'個人網站'})
            if node.xpath('td/text()').re(u'電子信箱'):
                for email in node.xpath('td/a/text()').re(u'[\s]*([\S]+)[\s]*'):
                    item['contact_details'].append({'type': 'email', 'label': u'電子信箱', 'value': email})
            if node.xpath('td/text()').re(u'電[\s]*話'):
                for phone in node.xpath('td/span/text()').extract():
                    item['contact_details'].append({'type': 'voice', 'label': u'電話', 'value': re.sub(u'\s', '', phone)})
            if node.xpath('td/text()').re(u'傳[\s]*真'):
                for phone in node.xpath('td/span/text()').extract():
                    item['contact_details'].append({'type': 'fax', 'label': u'傳真', 'value': re.sub(u'\s', '', phone)})
            if node.xpath('td/text()').re(u'通[\s]*訊[\s]*處'):
                for address in node.xpath('td/span/text()').extract():
                    item['contact_details'].append({'type': 'address', 'label': u'通訊處', 'value': re.sub(u'\s', '', address)})
            if node.xpath('td/text()').re(u'學[\s]*歷'):
                item['education'] = [re.sub(u'\s', '', x) for x in node.xpath('td/span/text()').extract()]
            if node.xpath('td/text()').re(u'經[\s]*歷'):
                item['experience'] = [re.sub(u'\s', '', x) for x in node.xpath('td/span/text()').extract()]
            if node.xpath('th/text()').re(u'政[\s]*見'):
                item['platform'] = [re.sub(u'\s', '', x) for x in node.xpath('../tr/td/span/text()').extract()]
            if node.xpath('th/text()').re(u'備[\s]*註'):
                item['remark'] = [re.sub(u'\s', '', x) for x in node.xpath('../tr/td/span/text()').extract()]
        item['election_year'] = '2010'
        item['in_office'] = True
        return item
