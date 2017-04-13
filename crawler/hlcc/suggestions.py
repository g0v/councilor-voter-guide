# -*- coding: utf-8 -*-
import os
import re
import urllib
from urlparse import urljoin
import subprocess

import scrapy


class Spider(scrapy.Spider):
    name = 'suggestions'
    start_urls = ["http://www1.hl.gov.tw/ousv/parliament/index.asp"]

    def parse(self, response):
        for node in response.xpath(u'//td[contains(text(), "年12月止")]'):
            url = node.xpath(u'following::a[1]/@href').extract_first()
            item = {}
            m = re.search(u'(?P<year>\d+)年12月止', node.xpath(u'text()').extract_first())
            item['year'] = int(m.group('year')) + 1911
            item['month_to'] = '12'
            item['month_from'] = '01'
            item['url'] = url
            item['file_ext'] = item['url'].split('.')[-1]
            cmd = u'mkdir -p ../../data/hlcc/suggestions/ && wget --heade="User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" -q -O ../../data/hlcc/suggestions/{year}_{month_from}-{month_to}.{file_ext} "{url}"'.format(**item)
            subprocess.call(cmd, shell=True)
            yield item
