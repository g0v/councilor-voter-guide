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
    allowed_domains = ["tncc.gov.tw"]
    start_urls = ["http://www.tncc.gov.tw",]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    output_path = common.meeting_minutes_output_path(county_abbr, election_year)
    ads = {'2010': 1, '2014': 2, '2018': 3}
    ad = ads[election_year]

    def parse(self, response):
        return response.follow(response.xpath(u'//a[re:test(., "^出版品$")]/@href').extract_first(), callback=self.parse_list)

    def parse_list(self, response):
        for tr in response.css('#table2 tr'):
            link = tr.xpath(u'descendant::a[re:test(., "^第%d屆")]/@href' % self.ad).extract_first()
            if link:
                item = {}
                item['election_year'] = self.election_year
                item['date'] = common.ROC2AD(tr.xpath('td[1]/text()').extract_first())
                item['meeting'] = tr.xpath('td[3]/descendant::a/text()').extract_first()
                item['meeting'] = item['meeting'].replace('.', u'、')
                item['download_url'] = urljoin(response.url, link)
                ext = item['download_url'].split('.')[-1]
                file_name = '%s.%s' % (item['meeting'], ext)
                cmd = 'mkdir -p %s && wget -c -O %s%s "%s"' % (self.output_path, self.output_path, file_name, item['download_url'])
                retcode = subprocess.call(cmd, shell=True)
                yield item
