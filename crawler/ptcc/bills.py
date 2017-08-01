# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
from urlparse import urljoin
import scrapy

import common


class Spider(scrapy.Spider):
    name = "bills"
    allowed_domains = ["ptcc.gov.tw", ]
    start_urls = ["http://www.ptcc.gov.tw"]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    ads = {'2005': 16, '2009': 17, '2014': 18, '2018': 19}
    ad = ads[election_year]


    def parse(self, response):
        return response.follow(response.xpath(u'//a[img[@id="topmenu03"]]/@href').extract_first(), callback=self.parse_tab)

    def parse_tab(self, response):
        return response.follow(response.xpath(u'//a[re:test(., "^議員介紹$")]/@href').extract_first(), callback=self.parse_query)

    def parse_query(self, response):
        for link in response.css('.list.borderleft a::attr(href)'):
            yield response.follow(link, callback=self.parse_profile)

    def parse_profile(self, response):
        for node in response.xpath(u'(//td[re:test(., "提[\s　]*案")]/following-sibling::td)[1]/descendant::tr[position()>1]'):
            item = {}
            item['election_year'] = self.election_year
            item['id'] = '%s-%s-%s' % (node.xpath('td[3]/b/text()').extract_first(), node.xpath('td[1]/text()').extract_first(), node.xpath('td[2]/text()').extract_first(), )
            item['abstract'] = node.xpath('td[3]/text()').extract_first()
            item['proposed_by'] = re.sub(u'(副?議長|議員)', '', response.xpath(u'//td[re:test(., "議員：")]')[-1].xpath('text()').extract_first().strip(u'議員：').strip()).strip().split(u'、')
            resolution = (node.xpath('td[4]/text()').extract_first() or '').strip()
            if resolution:
                item['motions'] = [dict(zip(['motion', 'resolution', 'date'], [u'決議', resolution, None]))]
            item['links'] = [
                {
                    'url': response.url,
                    'note': 'original'
                }
            ]
            yield item
