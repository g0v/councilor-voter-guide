# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
import subprocess
from urlparse import urljoin
import scrapy

import common


class Spider(scrapy.Spider):
    name = "meeting"
    allowed_domains = ["210.69.176.20"]
    start_urls = ["http://210.69.176.20:8080/Agenda/EFileSearch.aspx?FileGrpKind=2&h=600",]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    output_path = common.meeting_minutes_output_path(county_abbr, election_year)
    payload = {
        'btnCongress': u'大會',
        'txtPageSize': u'300',
    }

    def parse(self, response):
        return scrapy.FormRequest.from_response(response, response.url, formdata=self.payload, callback=self.parse_post)

    def parse_post(self, response):
        links = response.xpath('//table/tr/td/a[contains(@href, "EFileDetail.aspx")]/@href').extract()
        for link in links:
            yield response.follow(link, callback=self.parse_profile)

    def parse_profile(self, response):
        item = {}
        item['election_year'] = self.election_year
        nodes = response.xpath('//table/tbody/tr')
        ref = {
            u'屆別': {'key': 'sitting', 'path': 'td/span/text()'},
            u'類別': {'key': 'category', 'path': 'td/span/text()'},
            u'日期': {'key': 'date', 'path': 'td/span/text()'},
            u'資料名稱': {'key': 'meeting', 'path': 'td/span/text()'},
            u'檔案': {'key': 'download_url', 'path': 'td/a/@href', 'extra': 'http://obas_front.tcc.gov.tw:8080/Agenda/'},
        }
        for node in nodes:
            value = ref.get(node.xpath('th/text()').extract_first().strip())
            if value:
                item[value['key']] = '%s%s' % (value.get('extra', ''), node.xpath(value['path']).extract_first())
        item['date'] = common.ROC2AD(item['date'])
        ext = re.search(u'FileName=[\w\d]+\.(\w+)&', item['download_url']).group(1)
        file_name = '%s_%s.%s' % (item['sitting'], item['meeting'], ext)
        cmd = 'mkdir -p %s && wget -c -O %s%s "%s"' % (self.output_path, self.output_path, file_name, item['download_url'])
        retcode = subprocess.call(cmd, shell=True)
        return item
