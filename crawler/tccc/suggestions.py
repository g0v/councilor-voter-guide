# -*- coding: utf-8 -*-
import os
import re
import urllib
from urlparse import urljoin
import subprocess

import scrapy


class Spider(scrapy.Spider):
    name = 'suggestions'
    start_urls = ["http://www.taichung.gov.tw"]

    def parse(self, response):
        yield scrapy.Request(urljoin(response.url, response.xpath(u'//a[contains(text(), "議員建議")]/@href').extract_first()), callback=self.parse_opengov)

    def parse_opengov(self, response):
        yield scrapy.Request(urljoin(response.url, response.xpath(u'//a[contains(@title, "議員所提")]/@href').extract_first()), callback=self.parse_list)

    def parse_list(self, response):
        for node in response.xpath(u'//a[re:test(@title, "\d+[上下]半年")]'):
            item = {}
            m = re.search(u'(?P<year>\d+).*?(?P<season>[上下])半年', node.xpath('@title').extract_first())
            item['year'] = int(m.group('year')) + 1911
            if m.group('season') == u'上':
                item['month_to'] = '06'
                item['month_from'] = '01'
            else:
                item['month_to'] = '12'
                item['month_from'] = '07'
            if re.search(u'檔案下載', node.xpath('@title').extract_first()):
                item['url'] = urljoin(response.url, node.xpath('@href').extract_first())
                item['file_ext'] = item['url'].split('.')[-1]
                cmd = u'mkdir -p ../../data/tccc/suggestions/ && wget --heade="User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" -q -O ../../data/tccc/suggestions/{year}_{month_from}-{month_to}.{file_ext} "{url}"'.format(**item)
                subprocess.call(cmd, shell=True)
                yield item
            else:
                yield scrapy.Request(urljoin(response.url, node.xpath('@href').extract_first()), callback=self.parse_file)

    def parse_file(self, response):
        for node in response.css(u'.filename a'):
            item = {}
            m = re.search(u'(?P<year>\d+).*?(?P<season>[上下])半年', node.xpath('@title').extract_first())
            item['year'] = int(m.group('year')) + 1911
            if m.group('season') == u'上':
                item['month_to'] = '06'
                item['month_from'] = '01'
            else:
                item['month_to'] = '12'
                item['month_from'] = '07'
            item['url'] = urljoin(response.url, node.xpath('@href').extract_first())
            item['file_ext'] = item['url'].split('.')[-1]
            cmd = u'mkdir -p ../../data/tccc/suggestions/ && wget --heade="User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" -q -O ../../data/tccc/suggestions/{year}_{month_from}-{month_to}.{file_ext} "{url}"'.format(**item)
            subprocess.call(cmd, shell=True)
            yield item
