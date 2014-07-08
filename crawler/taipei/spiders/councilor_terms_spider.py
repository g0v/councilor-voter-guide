# -*- coding: utf-8 -*-
import re
import urllib
from urlparse import urljoin
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from taipei.items import Councilor


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
    name = "taipei_councilor_terms"
    allowed_domains = ["www.tcc.gov.tw"]
    urls_list = []
    for ad in range(9, 20):
        urls_list.append('http://www.tcc.gov.tw/TermIntro.aspx?Term_SN=%s' % ad)
    start_urls = urls_list

    def parse(self, response):
        sel = Selector(response)
        item = Councilor()
        item['ad'] = int(re.search(u'Term_SN=([\d]{1,2})', response.url).group(1)) - 8
        node = sel.xpath('//table/tr/td/a[contains(@id, "FormView1_first_list_HyperLink1")]')
        item['title'] = '議長'
        yield Request('http://www.tcc.gov.tw/%s' % re.sub('\^', '&', node.xpath('@href').re(u'Councilor.*')[0]), callback=self.parse_profile, meta={'item': item})
        node = sel.xpath('//table/tr/td/a[contains(@id, "FormView1_second_list_HyperLink1")]')
        item = Councilor()
        item['ad'] = int(re.search(u'Term_SN=([\d]{1,2})', response.url).group(1)) - 8
        item['title'] = '副議長'
        yield Request('http://www.tcc.gov.tw/%s' % re.sub('\^', '&', node.xpath('@href').re(u'Councilor.*')[0]), callback=self.parse_profile, meta={'item': item})
        nodes = sel.xpath('//table/tr/td/a[contains(@id, "FormView1_ALL_list_HyperLink1")]')
        for node in nodes:
            item = Councilor()
            item['ad'] = int(re.search(u'Term_SN=([\d]{1,2})', response.url).group(1)) - 8
            item['title'] = '議員'
            yield Request('http://www.tcc.gov.tw/%s' % re.sub('\^', '&', node.xpath('@href').re(u'Councilor.*')[0]), callback=self.parse_profile, meta={'item': item})

    def parse_profile(self, response):
        sel = Selector(response)
        item = response.meta['item']
        item['county'] = '臺北市'
        image = sel.xpath('//table/tr/td/div[@class="aldermans_photo"]/img/@src').extract()[0]
        item['image'] = urljoin(response.url, urllib.quote(image.encode('utf8')))
        item['in_office'] = True
        nodes = sel.xpath('//table[@class="aldermans_information"]/tr')
        for node in nodes:
            if node.xpath('td/text()').re(u'姓[\s]*名'):
                item['name'] = re.sub(u'\s|　', '', node.xpath('td/span/text()').extract()[0])
            if node.xpath('td/text()').re(u'性[\s]*別'):
                item['gender'] = node.xpath('td/span/text()').re(u'[\s]*([\S]+)[\s]*')[0]
            if node.xpath('td/text()').re(u'出[\s]*生'):
                item['birth'] = GetDate(node.xpath('td/span/text()').extract()[0])
            if node.xpath('td/text()').re(u'黨[\s]*籍'):
                item['party'] = node.xpath('td/span/text()').re(u'[\s]*([\S]+)[\s]*')[0]
            if node.xpath('td/text()').re(u'學[\s]*歷'):
                item['education'] = node.xpath('td/span/text()').extract()
            if node.xpath('td/text()').re(u'經[\s]*歷'):
                item['experience'] = node.xpath('td/span/text()').extract()
            if node.xpath('th/text()').re(u'備[\s]*註'):
                item['remark'] = node.xpath('../tr/td/span/text()').extract()
                item['term_end'] = {}
                item['term_end']['date'] = GetDate(node.xpath('../tr/td/span/text()').extract()[0])
                item['term_end']['reason'] = '\n'.join(item['remark'])
                item['in_office'] = False
        item['links'] = {'council': response.url}
        return item
