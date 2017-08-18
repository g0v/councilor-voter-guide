# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
from urlparse import urljoin
import time
import scrapy

import common


class Spider(scrapy.Spider):
    name = "bills"
    allowed_domains = ["kmcc.gov.tw", ]
    start_urls = ["http://www.kmcc.gov.tw"]
    download_delay = 3
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    ads = {'2009': 5, '2014': 6, '2018': 7}
    ad = ads[election_year]

    def parse(self, response):
        return response.follow(response.xpath(u'//a[re:test(., "^議事錄查詢$")]/@href').extract_first(), callback=self.parse_query)

    def parse_query(self, response):
        for bill_type in response.xpath(u'//select[@name="Type"]/option[re:test(., "(提案|請願)")]/@value').extract():
            for council in response.xpath(u'//select[@name="Council"]/option/@value').extract():
                payload = {
                    'Type': bill_type,
                    'Council': council
                }
                yield scrapy.FormRequest.from_response(response, formdata=payload, callback=self.parse_list, dont_filter=True, headers=common.headers(self.county_abbr))

    def parse_list(self, response):
        for link in response.css('.GridItem a::attr(href),.GridAlternatingItem a::attr(href)').extract():
            time.sleep(60)
            yield response.follow(link, callback=self.parse_profile)
        next_page = response.css(u'.GridPager span ~ a::attr(href)').extract_first()
        if next_page:
            payload = {'__EVENTTARGET': re.search("doPostBack\('([^']*)'", next_page).group(1)}
            yield scrapy.FormRequest.from_response(response, formdata=payload, callback=self.parse_list, dont_filter=True, dont_click=True, headers=common.headers(self.county_abbr))

    def parse_profile(self, response):
        item = {}
        item['election_year'] = self.election_year
        item['id'] = re.search('=([^&]*)', response.url).group(1).zfill(6)
        for key, label in [('type', u'Type'), ('category', u'Kind'), ('abstract', u'CasePoint'), ('description', u'CaseExplain'), ('methods', u'CaseMethod')]:
            content = response.css(u'#%s::text' % label).extract_first()
            if content:
                item[key] = content.strip()
        item['proposed_by'] = re.sub(u'(副?議長|議員)', '', response.css(u'#CaseUnit::text').extract_first()).strip().split(u'、')
        item['motions'] = []
        for motion, label in [(u'審查意見', 'CaseOpinion'), (u'大會決議', 'Resolution')]:
            resolution = response.css(u'#%s::text' % label).extract_first()
            if resolution:
                item['motions'].append(dict(zip(['motion', 'resolution', 'date'], [motion, resolution.strip(), None])))
        item['links'] = [
            {
                'url': response.url,
                'note': 'original'
            }
        ]
        return item
