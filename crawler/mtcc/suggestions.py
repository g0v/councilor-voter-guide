# -*- coding: utf-8 -*-
import os
import re
import urllib
from urlparse import urljoin
import subprocess

import scrapy


class Spider(scrapy.Spider):
    name = 'suggestions'
    start_urls = ["http://www.matsu.gov.tw/"]

    def parse(self, response):
        yield response.follow(response.xpath(u'//a[contains(@title, "議員所提")]/@href').extract_first(), callback=self.parse_file)

    def parse_file(self, response):
        for node in response.xpath(u'//a[re:test(@title, "\d+年度.*?議員所提")]'):
            item = {}
            label = node.xpath('@title').extract_first()
            if re.search(u'\d+\.06', label):
                continue
            m = re.search(u'(?P<year>\d+)年度', label)
            item['year'] = int(m.group('year')) + 1911
            item['month_from'] = '01'
            item['month_to'] = '12'
            item['url'] = urljoin(response.url, node.xpath('@href').extract_first())
            item['file_ext'] = 'ods' if re.search('Mcfile2', item['url']) else 'xls'
            cmd = u'mkdir -p ../../data/mtcc/suggestions/ && wget --heade="User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" -q -O ../../data/mtcc/suggestions/{year}_{month_from}-{month_to}.{file_ext} "{url}"'.format(**item)
            subprocess.call(cmd, shell=True)
            yield item
