# -*- coding: utf-8 -*-
import re
import urllib
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from cy.items import PropertyItem


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

class Spider(BaseSpider):
    name = "property"
    allowed_domains = ["sunshine.cy.gov.tw"]
    start_urls = ['http://sunshine.cy.gov.tw/GipOpenWeb/wSite/sp?xdUrl=/wSite/SpecialPublication/SpecificLP.jsp&ctNode=']
    def start_requests(self):
        payload = {
            'queryCol': u'period',
            'queryStr': u'',
            'perPage': u'300'
        }
        return [FormRequest("http://sunshine.cy.gov.tw/GipOpenWeb/wSite/sp?xdUrl=/wSite/SpecialPublication/SpecificLP.jsp&ctNode=", formdata=payload, callback=self.parse)]

    def parse(self, response):
        sel = Selector(response)
        trs = sel.xpath('//table[@class="lptb3"]/tbody/tr')
        for tr in trs:
            item = PropertyItem()
            tds = tr.xpath('td')
            if tds:
                attr = tds[1].xpath('a/@href').re("javascript:submitToBaseLp[(]'(\S+)','(\S+)'[)]")
                item['stage'] = tds[1].xpath('a/text()').extract()[0]
                item['date'] = GetDate(tds[3].xpath('text()').extract()[0])
                payload = {
                    'queryCol': attr[1],
                    'queryStr': attr[0],
                    'perPage': u'300'
                }
                yield FormRequest('http://sunshine.cy.gov.tw/GipOpenWeb/wSite/sp?xdUrl=/wSite/SpecialPublication/baseList.jsp&ctNode=', formdata=payload, callback=self.parse_profile, meta={'item': item})

    def parse_profile(self, response):
        sel = Selector(response)
        items = []
        trs = sel.xpath('//table[@class="lptb3"]/tbody/tr')
        for tr in trs:
            item = response.meta['item'].copy()
            tds = tr.xpath('td')
            if tds:
                try:
                    item['file_id'] = tds[1].xpath('a/@href').re(u"javascript[:]redirectFileDownload[(](\d+)[)]")[0]
                    item['download_url'] = 'http://sunshine.cy.gov.tw/GipOpenWeb/wSite/SpecialPublication/fileDownload.jsp?id=%s' % item['file_id']
                except:
                    item['download_url'] = ''
                item['name'] = tds[1].xpath('a/text()').re(u'\s*(\S+)\s*')[0]
                item['journal'] = tds[2].xpath('text()').re(u'\s*(\S+)\s*')[0]
                item['department'] = re.sub(u'\s', '', tds[3].xpath('text()').extract()[0])
                item['category'] = tds[4].xpath('text()').re(u'\s*(\S+)\s*')[0]
                item['publication_date'] = GetDate(tds[5].xpath('text()').extract()[0])
                item['at_page'] = tds[6].xpath('text()').re(u'\s*(\S+)\s*')[0]
                items.append(item)
        return items
