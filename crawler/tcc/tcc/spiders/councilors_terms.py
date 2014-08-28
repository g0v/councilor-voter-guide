# -*- coding: utf-8 -*-
import re
import urllib
from urlparse import urljoin
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from tcc.items import Councilor


def GetDate(text):
    matchTerm = re.search(u'''
        (?P<year>[\d]+)[\s]*(年|[.])[\s]*
        (?P<month>[\d]+)[\s]*(月|[.])[\s]*
        (?P<day>[\d]+)
    ''', text, re.X)
    if matchTerm:
        return '%04d-%02d-%02d' % (int(matchTerm.group('year'))+1911, int(matchTerm.group('month')), int(matchTerm.group('day')))
    else:
        return None

class Spider(scrapy.Spider):
    name = "councilors_terms"
    allowed_domains = ["www.tcc.gov.tw"]
    urls_list = []
    for ad in range(9, 20):
        urls_list.append('http://www.tcc.gov.tw/TermIntro.aspx?Term_SN=%s' % ad)
    start_urls = urls_list
    download_delay = 0.5

    def parse(self, response):
        sel = Selector(response)
        item = Councilor()
        ad = int(re.search(u'Term_SN=([\d]{1,2})', response.url).group(1)) - 8
        election_year = {1: '1969', 2: '1973', 3: '1977', 4: '1981', 5: '1985', 6: '1989', 7: '1994', 8: '1998', 9: '2002', 10: '2006', 11: '2010', 12: '2014'}
        node = sel.xpath('//table/tr/td/a[contains(@id, "FormView1_first_list_HyperLink1")]')
        item['election_year'] = election_year[ad]
        item['term_end'] = {'date': '%s-12-25' % election_year[ad+1]}
        item['title'] = '議長'
        yield Request('http://www.tcc.gov.tw/%s' % re.sub('\^', '&', node.xpath('@href').re(u'Councilor.*')[0]), callback=self.parse_profile, meta={'item': item})
        node = sel.xpath('//table/tr/td/a[contains(@id, "FormView1_second_list_HyperLink1")]')
        item = Councilor()
        item['election_year'] = election_year[ad]
        item['term_end'] = {'date': '%s-12-25' % election_year[ad+1]}
        item['title'] = '副議長'
        yield Request('http://www.tcc.gov.tw/%s' % re.sub('\^', '&', node.xpath('@href').re(u'Councilor.*')[0]), callback=self.parse_profile, meta={'item': item})
        nodes = sel.xpath('//table/tr/td/a[contains(@id, "FormView1_ALL_list_HyperLink1")]')
        for node in nodes:
            item = Councilor()
            item['election_year'] = election_year[ad]
            item['term_end'] = {'date': '%s-12-25' % election_year[ad+1]}
            item['title'] = '議員'
            yield Request('http://www.tcc.gov.tw/%s' % re.sub('\^', '&', node.xpath('@href').re(u'Councilor.*')[0]), callback=self.parse_profile, meta={'item': item})

    def parse_profile(self, response):
        sel = Selector(response)
        item = response.meta['item']
        item['term_start'] = '%s-12-25' % item['election_year']
        item['county'] = '臺北市'
        image = sel.xpath('//table/tr/td/div[@class="aldermans_photo"]/img/@src').extract()[0]
        item['image'] = urljoin(response.url, urllib.quote(image.encode('utf8')))
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        item['in_office'] = True
        nodes = sel.xpath('//table[@class="aldermans_information"]/tr')
        for node in nodes:
            if node.xpath('td/text()').re(u'姓[\s]*名'):
                item['name'] = re.sub(u'\s|　', '', node.xpath('td/span/text()').extract()[0])
            if node.xpath('td/text()').re(u'性[\s]*別'):
                item['gender'] = node.xpath('td/span/text()').re(u'[\s]*([\S]+)[\s]*')[0]
            if node.xpath('td/text()').re(u'出[\s]*生'):
                birth = node.xpath('td/span/text()').extract()
                item['birth'] = GetDate(birth[0]) if birth else None
            if node.xpath('td/text()').re(u'黨[\s]*籍'):
                item['party'] = node.xpath('td/span/text()').re(u'[\s]*([\S]+)[\s]*')[0]
            if node.xpath('td/text()').re(u'學[\s]*歷'):
                item['education'] = node.xpath('td/span/text()').extract()
            if node.xpath('td/text()').re(u'經[\s]*歷'):
                item['experience'] = node.xpath('td/span/text()').extract()
            if node.xpath('th/text()').re(u'備[\s]*註'):
                item['remark'] = node.xpath('../tr/td/span/text()').extract()
                if item['remark']:
                    item['term_end']['date'] = GetDate(node.xpath('../tr/td/span/text()').extract()[0]) or item['term_end']['date']
                    item['term_end']['reason'] = '\n'.join(item['remark'])
                    item['in_office'] = False
        return item
