# -*- coding: utf-8 -*-
import os
import re
import urllib
from urlparse import urljoin
import subprocess

import scrapy


class Spider(scrapy.Spider):
    name = 'suggestions'
    start_urls = ["http://www.yunlin.gov.tw"]

    def parse(self, response):
        yield scrapy.Request(urljoin(response.url, response.xpath(u'//a[text()="政府公開資訊"]/@href').extract_first()), callback=self.parse_opengov)

    def parse_opengov(self, response):
        url = response.xpath(u'//a[contains(text(), "議員建議")]/@href').extract_first()
        if url:
            yield scrapy.Request(urljoin(response.url, url), callback=self.parse_file)
        else:
            next_page = response.xpath(u'//a[contains(text(), "下一頁")]/@href').extract_first()
            yield scrapy.Request(urljoin(response.url, next_page), dont_filter=True, callback=self.parse_opengov)

    def parse_file(self, response):
        for node in response.xpath(u'//a[contains(@title, "議員所提")]'):
            item = {}
            m = re.search(u'(?P<year>\d+)年度?', node.xpath('@title').extract_first())
            item['year'] = int(m.group('year')) + 1911
            item['month_from'] = '01'
            item['month_to'] = '12'
            item['url'] = urljoin(response.url, node.xpath('@href').extract_first())
            item['file_ext'] = item['url'].split('.')[-1]
            cmd = u'mkdir -p ../../data/ylcc/suggestions/ && wget --heade="User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" -q -O ../../data/ylcc/suggestions/{year}_{month_from}-{month_to}.{file_ext} "{url}"'.format(**item)
            subprocess.call(cmd, shell=True)
            yield item
