# -*- coding: utf-8 -*-
import os
import re
import urllib
from urlparse import urljoin
import subprocess

import scrapy


class Spider(scrapy.Spider):
    name = 'suggestions'
    start_urls = ["http://www.nantou.gov.tw/big5/index.asp"]

    def parse(self, response):
        yield response.follow(response.xpath(u'//a[contains(@title, "議員所提")]/@href').extract_first(), callback=self.parse_list)

    def parse_list(self, response):
        for url in response.xpath(u'//a[@alt="檔案詳細內容"]/@href').extract():
            yield response.follow(url, callback=self.parse_file)

    def parse_file(self, response):
        for node in response.css('.content2 a'):
            item = {}
            label = node.xpath('following-sibling::font[1]/text()').extract_first()
            if re.search(u'年06月止', label):
                continue
            m = re.search(u'至(?P<year>\d+)年', label)
            item['year'] = int(m.group('year')) + 1911
            item['month_to'] = '12'
            item['month_from'] = '01'
            item['url'] = urljoin(response.url, node.xpath('@href').extract_first())
            item['file_ext'] = item['url'].split('.')[-1]
            cmd = u'mkdir -p ../../data/ntcc/suggestions/ && wget --no-check-certificate --heade="User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" -q -O ../../data/ntcc/suggestions/{year}_{month_from}-{month_to}.{file_ext} "{url}"'.format(**item)
            subprocess.call(cmd, shell=True)
            yield item
