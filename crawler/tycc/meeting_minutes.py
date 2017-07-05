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
    allowed_domains = ["www.tycc.gov.tw"]
    start_urls = ["http://www.tycc.gov.tw/content/public/public_main.aspx?wtp=1&wnd=217",]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    output_path = common.meeting_minutes_output_path(county_abbr, election_year)
    election_years_ad = {
        '2014': '1',
        '2010': '17'
    }
    ad = election_years_ad[election_year]

    def parse(self, response):
        nodes = response.xpath(u'//tr/td[re:test(@title, "第%s屆")]/following-sibling::td/a[re:test(., "會$")]' % self.ad)
        for node in nodes:
            item = {}
            item['election_year'] = self.election_year
            item['download_url'] = urljoin(response.url, node.xpath('@href').extract_first().strip())
            item['sitting'] = u'第%s屆' % self.ad
            item['meeting'] = node.xpath('descendant::*/text()').re(u'屆(.+會)$')[0]
            item['meeting'] = item['meeting'].replace('.', u'、')
            ext = node.xpath('@href').extract_first().split('.')[-1]
            file_name = '%s_%s.%s' % (item['sitting'], item['meeting'], ext)
            cmd = 'mkdir -p %s && wget -c -O %s%s "%s"' % (self.output_path, self.output_path, file_name, item['download_url'])
            retcode = subprocess.call(cmd, shell=True)
            yield item
        nodes = response.xpath(u'//tr/td[re:test(@title, "第%s屆")]/following-sibling::td/a[re:test(., "(冊|pdf)$")]' % self.ad)
        for node in nodes:
            item = {}
            item['election_year'] = self.election_year
            item['download_url'] = urljoin(response.url, node.xpath('@href').extract_first().strip())
            item['sitting'] = u'第%s屆' % self.ad
            item['meeting'] = '%s%s' % (node.xpath('preceding::td[1]/text()').re(u'屆(.+會)')[0], node.xpath('descendant::*/text()').re(u'(.+冊)')[0])
            item['meeting'] = item['meeting'].replace('.', u'、')
            ext = node.xpath('@href').extract_first().split('.')[-1]
            file_name = '%s_%s.%s' % (item['sitting'], item['meeting'], ext)
            cmd = 'mkdir -p %s && wget -c -O %s%s "%s"' % (self.output_path, self.output_path, file_name, item['download_url'])
            retcode = subprocess.call(cmd, shell=True)
            yield item
