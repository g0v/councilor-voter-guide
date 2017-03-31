# -*- coding: utf-8 -*-
import os
import re
import urllib
from urlparse import urljoin
import subprocess

import scrapy


class Spider(scrapy.Spider):
    name = 'suggestions'
    start_urls = ["http://dep-auditing.hccg.gov.tw"]

    def parse(self, response):
        yield scrapy.Request(urljoin(response.url, response.xpath(u'//a[@title="議員建議事項"]/@href').extract_first()), callback=self.parse_list)

    def parse_list(self, response):
        for url in response.xpath(u'//a[re:test(text(), "\d+月底議員建議事項")]/@href').extract():
            yield scrapy.Request(urljoin(response.url, url), callback=self.parse_file)

    def parse_file(self, response):
        item = {}
        title = response.css(u'.content_detail_title').extract_first()
        m = re.search(u'(?P<year>\d+)年.*?(?P<month_to>\d+)月', title)
        item['year'] = int(m.group('year')) + 1911
        item['month_to'] = m.group('month_to').zfill(2)
        item['month_from'] = '%02d' % (int(m.group('month_to')) - 5)
        for node in response.css('.div_file').xpath('a'):
            item['url'] = urljoin(response.url, node.xpath('@href').extract_first())
            item['file_ext'] = re.sub('[()\s]', '', node.xpath('text()').extract_first()).lower()
            cmd = u'mkdir -p ../../data/hsinchucc/suggestions/ && wget --heade="User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" -Nc -O ../../data/hsinchucc/suggestions/{year}_{month_from}-{month_to}.{file_ext} "{url}"'.format(**item)
            subprocess.call(cmd, shell=True)
            yield item
