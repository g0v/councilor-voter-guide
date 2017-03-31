# -*- coding: utf-8 -*-
import os
import re
import urllib
from urlparse import urljoin
import subprocess

import scrapy


class Spider(scrapy.Spider):
    name = 'suggestions'
    start_urls = ["http://civil.klcg.gov.tw/"]

    def parse(self, response):
        yield scrapy.Request(urljoin(response.url, response.xpath(u'//a[@title="主題服務"]/@href').extract_first()), callback=self.parse_opengov)

    def parse_opengov(self, response):
        yield scrapy.Request(urljoin(response.url, response.xpath(u'//a[contains(text(), "議員所提")]/@href').extract_first()), callback=self.parse_list)

    def parse_list(self, response):
        for url in response.css(u'a.row').xpath('@href').extract():
            yield scrapy.Request(urljoin(response.url, url), callback=self.parse_file)

    def parse_file(self, response):
        for node in response.xpath(u'//a[re:test(@title, "\d+年\s*\d+\s*至\s*\d+月")]'):
            item = {}
            m = re.search(u'(?P<year>\d+)年\s*(?P<month_from>\d+)\s*至+\s*(?P<month_to>\d+)月', node.xpath('@title').extract_first())
            item['year'] = int(m.group('year')) + 1911
            item['month_to'] = m.group('month_to').zfill(2)
            item['month_from'] = m.group('month_from').zfill(2)
            item['url'] = urljoin(response.url, node.xpath('@href').extract_first())
            item['file_ext'] = node.xpath('@title').extract_first().split('.')[-1]
            cmd = u'mkdir -p ../../data/kmc/suggestions/ && wget --heade="User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" -Nc -O ../../data/kmc/suggestions/{year}_{month_from}-{month_to}.{file_ext} "{url}"'.format(**item)
            subprocess.call(cmd, shell=True)
            yield item
        next_page = response.xpath(u'//*[@title="下一頁"]/parent::a/@href').extract_first()
        if next_page:
            yield scrapy.Request(urljoin(response.url, next_page), callback=self.parse_file)

