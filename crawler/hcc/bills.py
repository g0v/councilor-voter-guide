# -*- coding: utf-8 -*-
import re
import urllib
from urlparse import urljoin
from datetime import datetime
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy import log
from hcc.items import Bills


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
    name = "bills"
    allowed_domains = ["www.hcc.gov.tw"]
    start_urls = ["http://www.hcc.gov.tw/06board/03porposal_2.asp",]
    download_delay = 0.1

    election_year_map = [
        {
            "start": datetime(2006, 3, 1),
            "end": datetime(2010, 3, 1),
            "election_year": "2005"
        },
        {
            "start": datetime(2010, 3, 1),
            "end": datetime(2014, 12, 25),
            "election_year": "2009"
        }
    ]

    def parse(self, response):
        offset, pages = [int(x) for x in re.findall('\d+', response.xpath('//a[contains(@href, "/06board/03porposal_2")]')[-2].xpath('text()').extract()[0])]
        for i in range(0 ,offset*(pages+1), offset):
            yield Request('%s?offset=%d' % (response.url, i), callback=self.parse_page, dont_filter=True)

    def parse_page(self, response):
        items = []
        for tr in response.xpath('//tr[@class="line"]'):
            tds = tr.xpath('td[@valign="top"]')
            item = Bills()
            item['county'] = u'新竹縣'
            item['type'] = u'議員提案'
            item['id'] = tds[0].xpath('a/@href').extract()[0].split('/')[-1]
            item['links'] = urljoin(response.url, urllib.quote(tds[0].xpath('a/@href').extract()[0].encode('utf8')))
            abstract = tds[0].xpath('a/text()').extract()
            item['abstract'] = abstract[0].strip() if abstract else ''
            item['proposed_by'] = tds[1].xpath('text()').extract()[0].strip().rstrip(u',').split(u',')
            item['petitioned_by'] = tds[2].xpath('text()').extract()[0].strip().split(u',')
            date = datetime.strptime(tds[3].xpath('text()').extract()[0], '%Y-%m-%d')
            for term in self.election_year_map:
                if date >= term['start'] and date <= term['end']:
                    item['election_year'] = term['election_year']
                    break
            items.append(item)
        return items
