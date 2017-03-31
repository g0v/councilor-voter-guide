# -*- coding: utf-8 -*-
import os
import re
import urllib
from urlparse import urljoin
import subprocess

import scrapy


class Spider(scrapy.Spider):
    name = 'suggestions'
    start_urls = ["http://accounting.chcg.gov.tw"]

    def parse(self, response):
        yield scrapy.Request(urljoin(response.url, response.xpath(u'//a[contains(text(), "業務專區")]/@href').extract_first()), callback=self.parse_dep)

    def parse_dep(self, response):
        yield scrapy.Request(urljoin(response.url, response.xpath(u'//a[contains(text(), "預算、決算")]/@href').extract_first()), callback=self.parse_opengov)

    def parse_opengov(self, response):
        yield scrapy.Request(urljoin(response.url, response.xpath(u'//a[contains(text(), "公開資訊")]/@href').extract_first()), callback=self.parse_suggestions)

    def parse_suggestions(self, response):
        yield scrapy.Request(urljoin(response.url, response.xpath(u'//a[contains(., "議員所提")]')[-1].xpath('@href').extract_first()), callback=self.parse_file)

    def parse_file(self, response):
        for node in response.xpath(u'//*[re:test(text(), "\d+年對議員所提")]'):
            item = {}
            m = re.search(u'(?P<year>\d+)年', node.xpath('text()').extract_first())
            item['year'] = int(m.group('year')) + 1911
            item['month_to'] = '12'
            item['month_from'] = '01'
            item['url'] = urljoin(response.url, urllib.quote(node.xpath('following::a[1]/@href').extract_first().encode(response.encoding)))
            item['file_ext'] = item['url'].split('.')[-1]
            cmd = u'mkdir -p ../../data/chcc/suggestions/ && wget --heade="User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" -Nc -O ../../data/chcc/suggestions/{year}_{month_from}-{month_to}.{file_ext} "{url}"'.format(**item)
            subprocess.call(cmd, shell=True)
            yield item
