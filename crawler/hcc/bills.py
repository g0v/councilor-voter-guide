# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
from urlparse import urljoin
from datetime import datetime
import scrapy

import common


class Spider(scrapy.Spider):
    name = "bills"
    allowed_domains = ["www.hcc.gov.tw"]
    start_urls = ["http://www.hcc.gov.tw/",]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    election_year_map = {
        "2005": {
            "start": datetime(2006, 3, 1),
            "end": datetime(2010, 3, 1)
        },
        "2009": {
            "start": datetime(2010, 3, 1),
            "end": datetime(2014, 12, 25)
        },
        "2014": {
            "start": datetime(2014, 12, 25),
            "end": datetime(2018, 12, 25),
        },
        "2018": {
            "start": datetime(2018, 12, 25),
            "end": datetime(2022, 12, 25),
        },
    }
    term_range = election_year_map[election_year]

    def parse(self, response):
        return response.follow(response.xpath(u'//a[@title="議員提案"]/@href').extract_first(), callback=self.parse_page, meta={'type': u'議員提案'})

    def parse_page(self, response):
        bill_type = response.meta['type']
        for node in response.css('.list--table ul:not(:first-child)'):
            date = datetime.strptime(node.css('.date-list::text').extract_first(), '%Y-%m-%d')
            if date < self.term_range['start']:
                raise scrapy.exceptions.CloseSpider('out of date range')
            if date > self.term_range['end']: # continue to next page
                break
            item = {}
            item['election_year'] = self.election_year
            item['type'] = bill_type
            item['category'] = node.css(u'[data-th*="類別："]::text').extract_first()
            link = node.css('.more-list a::attr(href)').extract_first()
            item['id'] = link.split('=')[-1].zfill(6)
            item['abstract'] = node.css(u'[data-th*="案由："]::text').extract_first()
            item['proposed_by'] = (node.css(u'[data-th*="提案人："]::text').extract_first() or '').split()
            item['petitioned_by'] = (node.css(u'[data-th*="聯署人："]::text').extract_first() or '').split()
            yield response.follow(node.css('.more-list a::attr(href)').extract_first(), callback=self.parse_detail, meta={'item': item})
        if response.css('a.pager.pager-next[href]').extract():
            yield response.follow(response.css('a.pager.pager-next[href]::attr(href)').extract_first(), callback=self.parse_page, meta={'type': bill_type})

    def parse_detail(self, response):
        item = response.meta['item']
        item['links'] = [
            {
                'url': response.url,
                'note': 'original'
            }
        ]
        for link in response.css('.list--none.actions a::attr(href)').extract():
            item['links'].append(
                {
                    'url': urljoin(response.url, link),
                    'note': 'attach'
                }
            )
        return item
