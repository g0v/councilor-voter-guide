# -*- coding: utf-8 -*-
import os
import re
import json
import scrapy


class Spider(scrapy.Spider):
    name = "mayors"
    allowed_domains = ["db.cec.gov.tw"]
    start_urls = ["http://db.cec.gov.tw/",]
    download_delay = 1

    def parse(self, response):
        for level in response.xpath(u'//a[re:test(., "^2014.+(直轄|縣)市長選舉$")]/@href').extract():
            yield response.follow(level, callback=self.parse_level)

    def parse_level(self, response):
        yield response.follow(response.xpath(u'//a[re:test(., "候選人得票明細")]/@href').extract_first(), callback=self.parse_list)

    def parse_list(self, response):
        for tr in response.css(u'table.ctks tr.data'):
            d = {'county': tr.xpath('td[@rowspan]/a/text()').extract_first()}
            if d['county']:
                county = d['county']
                for i, key in enumerate(['number', 'gender', 'birth_year', 'party', 'votes', 'votes_percentage', 'elected', 'occupy'], start=3):
                    d[key] = tr.xpath('td[%d]/text()' % i).extract_first().strip()
                d['name'] = tr.xpath('td[2]/a/text()').extract_first().strip()
                yield response.follow(tr.xpath('td[2]/a/@href').extract_first(), callback=self.parse_person, meta={'meta': d})
            else:
                d['county'] = county
                for i, key in enumerate(['number', 'gender', 'birth_year', 'party', 'votes', 'votes_percentage', 'elected', 'occupy'], start=2):
                    d[key] = tr.xpath('td[%d]/text()' % i).extract_first().strip()
                d['name'] = tr.xpath('td[1]/a/text()').extract_first().strip()
                yield response.follow(tr.xpath('td[1]/a/@href').extract_first(), callback=self.parse_person, meta={'meta': d})

    def parse_person(self, response):
        d = response.meta['meta']
        d['votes_detail'] = []
        for tr in response.css(u'table.ctks tr.data'):
            d['votes_detail'].append({
                'district': re.sub(u'^%s' % d['county'], '', tr.xpath('td[1]/a/text()').extract_first()),
                'votes': tr.xpath('td[4]/text()').extract_first(),
                'votes_percentage': tr.xpath('td[5]/text()').extract_first().strip()
            })
        yield d
