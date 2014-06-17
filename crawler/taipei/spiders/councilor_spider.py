# -*- coding: utf-8 -*-
import re
import urllib
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from taipei.items import Councilor


def take_first(list_in):
    if len(list_in) == 1:
        return list_in[0]
    else:
        raise

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
    #for scrapy
    name = "taipei_councilor"
    allowed_domains = ["www.tcc.gov.tw"]
    start_urls = ["http://www.tcc.gov.tw/Councilor_Main.aspx",]

    def parse(self, response):
        """ get the following dictionary structure
            {
              name         :
              gender       :
              birth        :
              party        :
              constituency :
              county       :
              district     :
              contacts     :
              education    :
              experience   :
              platform     :
            }
        """
        sel = Selector(response)
        nodes = sel.xpath('//table/tr/td/a[contains(@href, "Councilor_Content.aspx")]')
        for node in nodes:
            yield Request('http://%s%s' % ("www.tcc.gov.tw/", take_first(node.xpath('@href').extract())), callback=self.parse_profile)

    def parse_profile(self, response):
        sel = Selector(response)
        item = Councilor()
        constituency = take_first(sel.xpath('//div/h3/span[@id="FormView1_ElectionZoneLabel"]/text()').extract())
        match = re.search(u'''
            第[\W]{1,3}屆
            (?P<county>[\W]{1,3}(?:縣|市))議員
            [\s]/[\s]
            (?P<selection>第[\W]{1,3}選區)
            [\s]
            （(?P<district>[\S]*)）
        ''', constituency, re.X)
        item['constituency'] = '%s%s' % (match.group('county'), match.group('selection'))
        item['county'] = match.group('county')
        item['district'] = match.group('district')
        nodes = sel.xpath('//table[@class="aldermans_information"]/tr')
        contacts = {}
        for node in nodes:
            if node.xpath('td/text()').re(u'姓[\s]*名'):
                item['name'] = take_first(node.xpath('td/span/text()').re(u'[\s]*([\S]+)[\s]*'))
            if node.xpath('td/text()').re(u'性[\s]*別'):
                item['gender'] = take_first(node.xpath('td/span/text()').re(u'[\s]*([\S]+)[\s]*'))
            if node.xpath('td/text()').re(u'出[\s]*生'):
                item['birth'] = GetDate(take_first(node.xpath('td/span/text()').extract()))
            if node.xpath('td/text()').re(u'黨[\s]*籍'):
                item['party'] = take_first(node.xpath('td/span/text()').re(u'[\s]*([\S]+)[\s]*'))
            if node.xpath('td/text()').re(u'電子信箱'):
                contacts['email'] = node.xpath('td/a/text()').extract()
            if node.xpath('td/text()').re(u'個人網站'):
                contacts['website'] = node.xpath('td/a/@href').extract()
            if node.xpath('td/text()').re(u'電[\s]*話'):
                contacts['phone'] = take_first(node.xpath('td/span/text()').extract()).replace('<br>', ' ').strip().split(' ')
            if node.xpath('td/text()').re(u'傳[\s]*真'):
                contacts['fax'] = take_first(node.xpath('td/span/text()').extract()).replace('<br>', ' ').strip().split(' ')
            if node.xpath('td/text()').re(u'通[\s]*訊[\s]*處'):
                contacts['address'] = take_first(node.xpath('td/span/text()').extract()).replace('<br>', ' ').strip().split(' ')
        item['contacts'] = contacts
        return item
