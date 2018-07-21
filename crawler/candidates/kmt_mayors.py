# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
import urllib
from urlparse import urljoin
import scrapy
import subprocess

import common


class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www1.kmt.org.tw"]
    start_urls = ["http://www1.kmt.org.tw/people.aspx?mid=236",]
    download_delay = 1

    def __init__(self, election_year=None, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.election_year = election_year
        self.path = u'../../data/avatar/mayors/%s/中國國民黨' % self.election_year

    def parse(self, response):
        links = response.css('.people_area a::attr(href)').extract()
        for link in links:
            yield response.follow(link, callback=self.parse_profile)

    def parse_profile(self, response):
        item = {}
        item['election_year'] = self.election_year
        item['name'] = response.css('#ctl00_ContentPlaceHolder1_CNAME::text').extract_first().strip()
        item['county'] = re.sub(u'長[候參]選人', '', response.css('#ctl00_ContentPlaceHolder1_CTCTITLE::text').extract_first().replace(u'台', u'臺'))
        item['education'] = u'\n'.join(response.css('#ctl00_ContentPlaceHolder1_EDUCATION::text').extract())
        item['experience'] = u'\n'.join(response.css('#ctl00_ContentPlaceHolder1_EXPERIENCE::text').extract())
        item['links'] = [
            {'url': urljoin(response.url, response.css('#ctl00_ContentPlaceHolder1_BLOG a::attr(href)').extract_first()), 'note': u'個人網站'},
            {'url': response.url, 'note': u'黨部候選人專區'}
        ]
        img_link = response.css('#ctl00_ContentPlaceHolder1_TR1 img::attr(src)').extract_first()
        f_name = '%s_%s.%s' % (item['county'], item['name'], img_link.split('.')[-1].split('?')[0])
        f = '%s/%s' % (self.path, f_name)
        if not os.path.isfile(f):
            cmd = 'wget --no-check-certificate "%s" -O %s' % (img_link, f)
            subprocess.call(cmd, shell=True)
        item['image'] = u'%s/%s/%s/%s/%s' % (common.storage_domain(), 'mayors', self.election_year, u'中國國民黨', f_name)
        return item
