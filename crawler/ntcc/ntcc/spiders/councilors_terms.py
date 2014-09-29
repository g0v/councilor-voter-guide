# -*- coding: utf-8 -*-
import re
import urllib
from urlparse import urljoin
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from ntcc.items import Councilor


def ROC2AD(text):
    matchTerm = re.search(u'''
        (?P<year>[\d]+)[\s]*(?:年|[-/.])[\s]*
        (?P<month>[\d]+)[\s]*(?:月|[-/.])[\s]*
        (?P<day>[\d]+)
    ''', text, re.X)
    if matchTerm:
        return '%04d-%02d-%02d' % (int(matchTerm.group('year'))+1911, int(matchTerm.group('month')), int(matchTerm.group('day')))
    else:
        return None

class Spider(scrapy.Spider):
    name = "councilors_terms"
    allowed_domains = ["www.ntp.gov.tw"]
    start_urls = ['http://www.ntp.gov.tw/content/history/history01-5.aspx']
    download_delay = 0.5

    def parse(self, response):
        sel = Selector(response)
        nodes = sel.xpath('//select[@id="ddlselect"]/option')
        for node in nodes:
            yield Request('http://www.ntp.gov.tw/content/history/history01-5.aspx?sid=%s' % node.xpath('@value').extract()[0], callback=self.parse_ad)

    def parse_ad(self, response):
        sel = Selector(response)
        ad_meta = sel.xpath('//table/tr/th/following-sibling::td[1]/text()').extract()
        term_start = ROC2AD(ad_meta[0].split(u'~')[0])
        term_end = ROC2AD(ad_meta[0].split(u'~')[1])
        chair = dict(zip(ad_meta[1:3], [u'議長', u'副議長']))
        nodes = sel.xpath('//a[contains(@href, "history01-5-p.aspx")]')
        for node in nodes:
            item = Councilor()
            item['election_year'] = term_start.split('-')[0]
            item['county'] = u'新北市'
            item['term_end'] = {'date': term_end}
            item['term_start'] = term_start
            item['name'] = node.xpath('text()').extract()[0].strip()
            item['title'] = u'議員'
            for name, title in chair.items():
                if name == item['name']:
                    item['title'] = title
            yield Request('http://www.ntp.gov.tw/content/history/%s' % node.xpath('@href').extract()[0], callback=self.parse_profile, meta={'item': item, 'term_range_ROC': ad_meta[0]}, dont_filter=True)

    def parse_profile(self, response):
        sel = Selector(response)
        item = response.meta['item']
        image = sel.xpath(u'//table/tr/td/img[contains(@alt, "大頭照")]/@src').extract()[0]
        item['image'] = urljoin(response.url, urllib.quote(image.encode('utf8')))
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        item['in_office'] = True
        nodes = sel.xpath('//table/tr/td')
        for i in range(0, len(nodes)):
            if nodes[i].xpath('text()').re(response.meta['term_range_ROC']):
                next_node = nodes[i+1].xpath('text()').extract()
                item['constituency'] = next_node[0]
                item['district'] = re.sub(u'[()]', '', next_node[1]) if len(next_node) > 1 else ''
                break
        nodes = sel.xpath('//div[@id="bg3"]/table')
        for node in nodes:
            if node.xpath('tr/td/img/@alt').re(u'學歷'):
                item['education'] = [line.strip() for line in node.xpath('tr/td/table/tr/td/text()').extract()]
            elif node.xpath('tr/td/img/@alt').re(u'經歷'):
                item['experience'] = [line.strip() for line in node.xpath('tr/td/table/tr/td/text()').extract()]
        return item
