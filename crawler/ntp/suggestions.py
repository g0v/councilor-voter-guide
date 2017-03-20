# -*- coding: utf-8 -*-
import os
import re
import urllib
from urlparse import urljoin
import subprocess

import scrapy


class Spider(scrapy.Spider):
    name = 'suggestions'
    start_urls = ["http://www.bas.ntpc.gov.tw/"]

    def parse(self, response):
        yield scrapy.Request(urljoin(response.url, response.xpath(u'//a[@title="政府資訊公開"]/@href').extract_first()), callback=self.parse_opengov)

    def parse_opengov(self, response):
        yield scrapy.Request(response.xpath(u'//a[@title="議員所提地方建設建議事項"]/@href').extract_first(), callback=self.parse_file)

    def parse_file(self, response):
        for node in response.xpath(u'//a[contains(@title, "議員所提")]'):
            item = {}
            m = re.search(u'(?P<year>\d+)年度(?P<month_from>\d+)\s*[-~]+\s*(?P<month_to>\d+)月', node.xpath('normalize-space(string())').extract_first())
            item['year'] = int(m.group('year')) + 1911
            item['month_from'] = m.group('month_from').zfill(2)
            item['month_to'] = m.group('month_to').zfill(2)
            item['url'] = urljoin(response.url, node.xpath('@href').extract_first())
            item['file_ext'] = item['url'].split('.')[-1]
            cmd = u'mkdir -p ../../data/ntp/suggestions/ && wget --heade="User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" -Nc -O ../../data/ntp/suggestions/{year}_{month_from}-{month_to}.{file_ext} "{url}"'.format(**item)
            subprocess.call(cmd, shell=True)
            yield item
