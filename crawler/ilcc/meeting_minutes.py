# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
import subprocess
from urlparse import urljoin
import logging
import scrapy

import common


class Spider(scrapy.Spider):
    name = "meeting"
    allowed_domains = ["www.ilcc.gov.tw"]
    start_urls = ["http://www.ilcc.gov.tw/Html/H_06/H_06.asp",]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    output_path = common.meeting_minutes_output_path(county_abbr, election_year)
    payload = {
        'ddlcounciltype': u'大會',
    }

    def parse(self, response):
        return response.follow(response.xpath(u'//area[@alt="會議紀錄"]/@href').extract_first(), callback=self.parse_frame)

    def parse_frame(self, response):
        return response.follow(response.xpath('//frame[@id="FrMain"]/@src').extract_first(), callback=self.parse_meeting_info)

    def parse_meeting_info(self, response):
        return scrapy.FormRequest.from_response(response, response.url, formdata=self.payload, callback=self.parse_pages)

    def parse_pages(self, response):
        pages = response.xpath('//select[@name="page"]/option/@value').extract()
        for page in pages:
            yield scrapy.FormRequest.from_response(response, response.url, formdata={'page': page, 'btSearch': None}, callback=self.parse_post)

    def parse_post(self, response):
        trs = response.xpath('//table[@id="dg"]/descendant::tr[position()>1]')
        for tr in trs:
            item = {}
            item['election_year'] = self.election_year
            item['date'] = re.sub('\s', '', tr.xpath('string(td[1])').extract_first())
            item['sitting'] = re.sub('\s', '', '%s%s' % (tr.xpath('string(td[2])').extract_first(), tr.xpath('string(td[3])').extract_first()))
            item['meeting'] = re.sub('\s', '', tr.xpath('string(td[5])').extract_first())
            yield response.follow(tr.xpath('td[4]/descendant::a/@href').extract_first(), callback=self.parse_profile, meta={'item': item})

    def parse_profile(self, response):
        item = response.meta['item']
        item['download_url'] = response.xpath('//td/a[@target="_blank"]/@href').extract_first()
        if item['download_url']:
            ext = re.search(u'\.(\w+)$', item['download_url']).group(1)
            file_name = '%s_%s.%s' % (item['sitting'], item['meeting'], ext)
            cmd = 'mkdir -p %s && wget -c -O %s%s "%s"' % (self.output_path, self.output_path, file_name, item['download_url'])
            retcode = subprocess.call(cmd, shell=True)
        else:
            logging.error(response.url)
        return item
