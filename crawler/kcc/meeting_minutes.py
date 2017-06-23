# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
import time
import subprocess
from urlparse import urljoin
import scrapy

import common


class Spider(scrapy.Spider):
    name = "meeting"
    allowed_domains = ["cissearch.kcc.gov.tw"]
    start_urls = ["http://cissearch.kcc.gov.tw/System/MeetingRecord/Default.aspx",]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    output_path = common.meeting_minutes_output_path(county_abbr, election_year)

    def parse(self, response):
        count = response.xpath('//span[@id="ContentPlaceHolder1_DataPager1"]/text()').re(u'共\s*(\d+)\s*筆')[0]
        payload = {'ctl00$ContentPlaceHolder1$DataPager1$ctl02$txtPageSize': count}
        yield scrapy.FormRequest.from_response(response, response.url, formdata=payload, callback=self.parse_profile, dont_filter=True)

    def parse_profile(self, response):
        trs = response.xpath('//table[@id="ContentPlaceHolder1_gvIndex"]/tr')
        for tr in trs:
            item = {}
            tds = tr.xpath('td')
            if tds:
                item['election_year'] = self.election_year
                item['date'] = common.ROC2AD(tds[1].xpath('text()').extract_first())
                meeting = tds[2].xpath('text()').extract_first()
                item['meeting'] = tds[2].xpath('text()').re(u'(.+?)[紀記][錄錄]')[0]
                item['download_url'] = urljoin(response.url, tds[3].xpath('a/@href').extract_first().strip())
                ext = item['download_url'].split('.')[-1]
                file_name = '%s.%s' % (item['meeting'], ext)
                cmd = 'mkdir -p %s && wget -c -O %s%s "%s"' % (self.output_path, self.output_path, file_name, item['download_url'])
                retcode = subprocess.call(cmd, shell=True)
                time.sleep(1)
                yield item
