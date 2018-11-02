# -*- coding: utf-8 -*-
import os
import re
import urllib
from urlparse import urljoin
import subprocess

import scrapy


class Spider(scrapy.Spider):
    name = 'suggestions'
    start_urls = ["http://www.kinmen.gov.tw"]

    def parse(self, response):
        yield response.follow(response.xpath(u'//a[contains(text(), "議員所提")]/@href').extract_first(), callback=self.parse_link)

    def parse_link(self, response):
        yield response.follow(response.css('.file-download .link a::attr(href)').extract_first(), callback=self.parse_list)

    def parse_list(self, response):
        for node in response.xpath(u'//a[contains(text(), "(年報)")]'):
            item = {}
            m = re.search(u'(?P<year>\d+)年度', node.xpath('text()').extract_first())
            item['year'] = int(m.group('year')) + 1911
            item['month_from'] = '01'
            item['month_to'] = '12'
            yield response.follow(node.xpath(u'@href').extract_first(), callback=self.parse_file, meta={'item': item})

    def parse_file(self, response):
        item = response.meta['item']
        for node in response.xpath(u'//a[contains(text(), "議員所提")]'):
            yield scrapy.Request(urljoin(response.url, node.xpath(u'@href').extract_first()), callback=self.parse_download, meta={'item': item})

    def parse_download(self, response):
        item = response.meta['item']
        item['url'] = response.url
        item['file_ext'] = response.headers['Content-Disposition'].split('.')[-1].strip('"')
        cmd = u'mkdir -p ../../data/kmcc/suggestions/ && wget --heade="User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" -q -O ../../data/kmcc/suggestions/{year}_{month_from}-{month_to}.{file_ext} "{url}"'.format(**item)
        subprocess.call(cmd, shell=True)
        yield item
