# -*- coding: utf-8 -*-
import os
import re
import urllib
from urlparse import urljoin
import subprocess

import scrapy


class Spider(scrapy.Spider):
    name = 'suggestions'
    start_urls = ["http://www.pthg.gov.tw"]

    def parse(self, response):
        yield scrapy.Request(urljoin(response.url, response.xpath(u'//a[contains(text(), "議員建議")]/@href').extract_first()), callback=self.parse_list)

    def parse_list(self, response):
        for url in response.css(u'a.css_mark').xpath('@href').extract():
            yield scrapy.Request(urljoin(response.url, url), callback=self.parse_file)

    def parse_file(self, response):
        year = response.xpath(u'//*[text()="年份"]/following::span[1]/text()').extract_first()

        for node in response.xpath(u'//th[contains(text(), "相關檔案")]/following::tr[1]//a'):
            item = {}
            item['year'] = int(year) + 1911
            item['month_to'] = '12'
            item['month_from'] = '01'
            item['url'] = urljoin(response.url, node.xpath('@href').extract_first())
            item['file_ext'] = item['url'].split('.')[-1]
            cmd = u'mkdir -p ../../data/ptcc/suggestions/ && wget --heade="User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" -Nc -O ../../data/ptcc/suggestions/{year}_{month_from}-{month_to}.{file_ext} "{url}"'.format(**item)
            subprocess.call(cmd, shell=True)
            yield item
