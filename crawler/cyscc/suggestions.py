# -*- coding: utf-8 -*-
import os
import re
import urllib
from urlparse import urljoin
import subprocess

import scrapy


class Spider(scrapy.Spider):
    name = 'suggestions'
    start_urls = ["http://accounting.cyhg.gov.tw/"]

    def parse(self, response):
        yield scrapy.Request(urljoin(response.url, response.xpath(u'//a[contains(@title, "議員所提")]/@href').extract_first()), callback=self.parse_list)

    def parse_list(self, response):
        for node in response.xpath(u'//a[re:test(@title, "\d+年度.*?議員所提")]'):
            item = {}
            m = re.search(u'(?P<year>\d+)年度.*?(?P<season>[上下])半年', node.xpath('text()').extract_first())
            item['year'] = int(m.group('year')) + 1911
            if m.group('season') == u'上':
                item['month_to'] = '06'
                item['month_from'] = '01'
            else:
                item['month_to'] = '12'
                item['month_from'] = '07'
            yield scrapy.Request(urljoin(response.url, node.xpath(u'@href').extract_first()), callback=self.parse_file, meta={'item': item})

    def parse_file(self, response):
        item = response.meta['item']
        for node in response.xpath(u'//a[re:test(@title, "\d+年度.*?議員所提")]'):
            item['url'] = urljoin(response.url, node.xpath('@href').extract_first())
            item['file_ext'] = item['url'].split('.')[-1]
            cmd = u'mkdir -p ../../data/cyscc/suggestions/ && wget --heade="User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" -q -O ../../data/cyscc/suggestions/{year}_{month_from}-{month_to}.{file_ext} "{url}"'.format(**item)
            subprocess.call(cmd, shell=True)
            yield item
