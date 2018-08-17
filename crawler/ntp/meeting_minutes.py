# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
import codecs
import subprocess
from urlparse import urljoin
import scrapy

import common


def write_file(data, file_name):
    file = codecs.open(file_name, 'w', encoding='utf-8')
    file.write(data)
    file.close()

class Spider(scrapy.Spider):
    name = "meeting"
    allowed_domains = ["www.ntp.gov.tw"]
    start_urls = ['https://www.ntp.gov.tw/content/information/information04.aspx']
    download_delay = 1
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    output_path = common.meeting_minutes_output_path(county_abbr, election_year)

    def parse(self, response):
        for node in response.xpath(u'//a[contains(@title, "HTML檔")]/@href').extract():
            yield response.follow(node, callback=self.parse_sitting)

    def parse_sitting(self, response):
        for node in response.xpath(u'//td/descendant::a/@href').extract():
            yield response.follow(node, callback=self.parse_meeting)

    def parse_meeting(self, response):
        try:
            sitting = response.xpath('//text()').re(u'(.+)日程表')[0]
            trs = [tr for tr in response.xpath('//table/descendant::tr') if tr.xpath('td[3]/text()').re('\d+')]
            for tr in trs:
                item = {}
                item['election_year'] = self.election_year
                item['date'] = common.ROC2AD(tr.xpath('td[1]/text()').extract_first())
                item['sitting'] = sitting
                item['meeting'] = tr.xpath('td[3]/text()').extract_first()
                item['download_url'] = tr.xpath('td[6]/descendant::a[1]/@href').extract_first()
                ext = item['download_url'].split('.')[-1]
                file_name = '%s_%s.%s' % (item['sitting'], item['meeting'], ext)
                if ext == 'pdf':
                    yield response.follow(item['download_url'], callback=self.download_pdf, meta={'item': item, 'file_name': file_name})
                elif ext == 'htm':
                    yield response.follow(item['download_url'], callback=self.parse_html, meta={'item': item, 'file_name': file_name})
        except scrapy.exceptions.NotSupported:
            pass

    def download_pdf(self, response):
        item = response.meta['item']
        item['download_url'] = response.url
        cmd = 'mkdir -p %s && wget --no-check-certificate -c -O %s%s "%s"' % (self.output_path, self.output_path, response.meta['file_name'], item['download_url'])
        retcode = subprocess.call(cmd, shell=True)
        return item

    def parse_html(self, response):
        item = response.meta['item']
        item['download_url'] = response.url
        text = '\n'.join(response.xpath('//pre/text()').extract())
        write_file(text, '%s%s_%s.txt' % (self.output_path, item['sitting'], item['meeting']))
        return item
