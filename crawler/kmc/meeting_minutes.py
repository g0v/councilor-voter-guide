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
    allowed_domains = ["www.kmc.gov.tw", "ebook.21cms.tw"]
    start_urls = ["http://www.kmc.gov.tw/recorder",]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    output_path = common.meeting_minutes_output_path(county_abbr, election_year)
    ads = {
        '2014': u'第十八屆',
        '2009': u'第十七屆'
    }
    ad = ads[election_year]

    def parse(self, response):
        nodes = response.css('.panel-body').xpath(u'descendant::a[re:test(., "%s")]' % self.ad)
        for node in nodes:
            link = node.xpath('@href').extract_first()
            item = {}
            item['election_year'] = self.election_year
            item['sitting'] = node.xpath('text()').extract_first().replace(u'(點擊閱讀)', '').replace('>>', '')
            item['download_url'] = urljoin(response.url, link)
            if re.search('/ebook/', link):
                file_name = '%s.pdf' % (item['sitting'], )
                cmd = 'mkdir -p %s && wget -A pdf -nd -r --no-parent -O "%s%s" "%s"' % (self.output_path, self.output_path, file_name, urljoin(response.url, link))
                retcode = subprocess.call(cmd, shell=True)
                yield item
            else:
                yield response.follow(link, callback=self.parse_iframe, meta={'item': item})

    def parse_iframe(self, response):
        link = response.css('.article-content iframe').xpath('@src').extract_first()
        item = response.meta['item']
        file_name = '%s.pdf' % (item['sitting'], )
        cmd = 'mkdir -p %s && wget -A pdf -nd -r --no-parent -O "%s%s" "%s"' % (self.output_path, self.output_path, file_name, link)
        retcode = subprocess.call(cmd, shell=True)
        yield item

