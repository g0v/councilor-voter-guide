# -*- coding: utf-8 -*-
import os
import re
import urllib
from urlparse import urljoin
import subprocess

import scrapy


class Spider(scrapy.Spider):
    name = 'suggestions'
    start_urls = ["http://www.hsinchu.gov.tw/"]

    def parse(self, response):
        yield scrapy.Request(urljoin(response.url, response.xpath(u'//a[@title="議員地方建設建議事項"]/@href').extract_first()), callback=self.parse_file)

    def parse_file(self, response):
        for node in response.xpath(u'//input[@value="EXCEL" or @value="PDF"]'):
            item = {}
            m = re.search(u'(?P<year>\d+)年度.*?(?P<season>(上半|下半))年度', node.xpath('preceding::a[1]/text()').extract_first())
            item['year'] = int(m.group('year')) + 1911
            if m.group('season') == u'上半':
                item['month_to'] = '06'
                item['month_from'] = '01'
            else:
                item['month_to'] = '12'
                item['month_from'] = '07'
            open_path = re.search(u"window.open\('(.+)'\);", node.xpath('@onclick').extract_first()).group(1)
            item['url'] = urljoin(response.url, open_path)
            item['file_ext'] = open_path.split('.')[-1]
            cmd = u'mkdir -p ../../data/hcc/suggestions/ && wget --heade="User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" -Nc -O ../../data/hcc/suggestions/{year}_{month_from}-{month_to}.{file_ext} "{url}"'.format(**item)
            subprocess.call(cmd, shell=True)
            yield item
