# -*- coding: utf-8 -*-
import os
import re
import urllib
from urlparse import urljoin
import subprocess

import scrapy


class Spider(scrapy.Spider):
    name = 'suggestions'
    start_urls = ["http://bgacst.e-land.gov.tw"]

    def parse(self, response):
        yield scrapy.Request(urljoin(response.url, response.xpath(u'//a[contains(text(), "議員建議")]/@href').extract_first()), callback=self.parse_list)

    def parse_list(self, response):
        for node in response.css(u'a.css_mark'):
            item = {}
            m = re.search(u'(?P<year>\d+)年度第(?P<season>[一二三四])季', node.xpath('text()').extract_first())
            item['year'] = int(m.group('year')) + 1911
            if re.search(u'[一二]', m.group('season')):
                item['month_to'] = '06'
                item['month_from'] = '01'
            else:
                item['month_to'] = '12'
                item['month_from'] = '07'
            yield scrapy.Request(urljoin(response.url, node.xpath('@href').extract_first()), callback=self.parse_file, meta={'item': item})

    def parse_file(self, response):
        item = response.meta['item']
        for node in response.xpath(u'//a[contains(@alt,"議員建議案")]'):
            item['url'] = node.xpath('@href').extract_first()
            item['file_ext'] = node.xpath('@alt').extract_first().split('.')[-1]
            cmd = u'mkdir -p ../../data/ilcc/suggestions/ && wget --heade="User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" -Nc -O ../../data/ilcc/suggestions/{year}_{month_from}-{month_to}.{file_ext} "{url}"'.format(**item)
            subprocess.call(cmd, shell=True)
            yield item
