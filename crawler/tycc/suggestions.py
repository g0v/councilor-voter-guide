# -*- coding: utf-8 -*-
import os
import re
import urllib
from urlparse import urljoin
import subprocess

import scrapy


class Spider(scrapy.Spider):
    name = 'suggestions'
    start_urls = ["http://dbas.tycg.gov.tw/"]

    def parse(self, response):
        yield scrapy.Request(response.xpath(u'//img[contains(@alt, "議員")]/parent::a/@href').extract_first(), callback=self.parse_route)

    def parse_route(self, response):
        yield scrapy.Request(urljoin(response.url, response.xpath(u'//a[re:test(text(), "議員.*?事項處理明細")]/@href').extract_first()), callback=self.parse_suggestions)

    def parse_suggestions(self, response):
        for url in response.xpath(u'//a[contains(@title, "本府對議員所提")]/@href').extract():
            yield scrapy.Request(urljoin(response.url, url), callback=self.parse_file)

    def parse_file(self, response):
        for node in response.xpath(u'//a[contains(@title, "議員所提")]'):
            item = {}
            m = re.search(u'(?P<year>\d+)年度(?P<month_from>\d+)\s*[-~]+\s*(?P<month_to>\d+)月', node.xpath('normalize-space(string())').extract_first())
            if m:
                item['year'] = int(m.group('year')) + 1911
                item['month_from'] = m.group('month_from').zfill(2)
                item['month_to'] = m.group('month_to').zfill(2)
            else:
                m = re.search(u'(?P<year>\d+)年度.*至.*?(?P<month_to>\d+)月', node.xpath('normalize-space(string())').extract_first())
                item['year'] = int(m.group('year')) + 1911
                item['month_from'] = '01'
                item['month_to'] = m.group('month_to').zfill(2)
            item['url'] = urljoin(response.url, node.xpath('@href').extract_first())
            item['file_ext'] = node.xpath('text()').extract_first().split('.')[-1].strip()
            cmd = u'mkdir -p ../../data/tycc/suggestions/ && wget --heade="User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" -Nc -O ../../data/tycc/suggestions/{year}_{month_from}-{month_to}.{file_ext} "{url}"'.format(**item)
            subprocess.call(cmd, shell=True)
            yield item
