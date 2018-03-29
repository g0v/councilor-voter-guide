# -*- coding: utf-8 -*-
import os
import re
import urllib
from urlparse import urljoin
import subprocess

import scrapy


class Spider(scrapy.Spider):
    name = 'suggestions'
    start_urls = ["http://www.penghu.gov.tw"]

    def parse(self, response):
        yield response.follow(response.xpath(u'//img[contains(@alt, "議員所提")]/parent::a/@href').extract_first(), callback=self.parse_list)

    def parse_list(self, response):
        for node in response.css('.list > a'):
            item = {}
            m = re.search(u'(?P<year>\d+)年.*?((?P<season>[上下])半年)?', node.xpath('@title').extract_first())
            item['year'] = int(m.group('year')) + 1911
            if m.group('season'):
                if m.group('season') == u'上':
                    item['month_to'] = '06'
                    item['month_from'] = '01'
                else:
                    item['month_to'] = '12'
                    item['month_from'] = '07'
            else:
                item['month_from'] = '01'
                item['month_to'] = '12'
            yield response.follow(node.xpath(u'@href').extract_first(), callback=self.parse_file, meta={'item': item})
        next_page = response.xpath(u'//a[@title="下一頁"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse_list)

    def parse_file(self, response):
        item = response.meta['item']
        for node in response.css('.icon a'):
            item['url'] = urljoin(response.url, node.xpath('@href').extract_first())
            item['file_ext'] = re.sub('[^.\w]', '', node.xpath('parent::span[1]/@title').extract_first()).split('.')[-1].lower()
            cmd = u'mkdir -p ../../data/phcouncil/suggestions/ && wget --heade="User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" -q -O ../../data/phcouncil/suggestions/{year}_{month_from}-{month_to}.{file_ext} "{url}"'.format(**item)
            subprocess.call(cmd, shell=True)
            yield item
