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
    allowed_domains = ["cyscc.gov.tw", ]
    start_urls = ["http://www.cyscc.gov.tw"]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    ads = {'2009': 17, '2014': 18, '2018': 19}
    ad = ads[election_year]

    def parse(self, response):
        return response.follow(response.xpath(u'//a[re:test(., "^議會資料庫$")]/@href').extract_first(), callback=self.parse_tab)

    def parse_tab(self, response):
        return response.follow(response.xpath(u'//a[re:test(., "^議會資料庫查詢系統$")]/@href').extract_first(), callback=self.parse_query)

    def parse_query(self, response):
        for value in response.xpath(u'//input[@name="ctl00$ContentPlaceHolder1$rbtnMKind"]/@value').extract():
            payload = {'ctl00$ContentPlaceHolder1$rbtnMKind': value}
            yield scrapy.FormRequest.from_response(response, formdata=payload, callback=self.parse_list, dont_filter=True, dont_click=True, headers=common.headers(self.county_abbr))

    def parse_list(self, response):
        pages = response.css('#ctl00_ContentPlaceHolder1_gvIndex_ctl13_lblPageCount::text').extract_first()
        print pages
        for node in response.css('.main3_3_04,.main3_3_05'):
            node_ad = int(node.xpath('td[2]/text()').re(u'(\d+)\s*屆')[0])
            if node_ad < self.ad:
                break
            if node_ad > self.ad:
                continue
            yield response.follow(node.xpath('td[6]/span/a/@href').extract_first(), callback=self.parse_profile)
        next_page = response.xpath(u'//a[re:test(.,"下一頁")]/@href').extract_first()
        if next_page and node_ad >= self.ad:
            payload = {'__EVENTTARGET': re.search("doPostBack\('([^']*)'", next_page).group(1)}
            yield scrapy.FormRequest.from_response(response, formdata=payload, callback=self.parse_list, dont_filter=True, dont_click=True, headers=common.headers(self.county_abbr))

    def parse_profile(self, response):
        item = {}
        item['election_year'] = self.election_year
        item['id'] = re.search('=([^&]*)', response.url).group(1).zfill(6)
        for key, label in [('type', u'提案類別'), ('category', u'類別'), ('abstract', u'案由'), ('description', u'說明'), ('methods', u'辦法')]:
                content = response.xpath(u'(//td[re:test(., "^%s$")]/following-sibling::td)[1]/span/text()' % label).extract_first()
                if content:
                    item[key] = content.strip()
        item['proposed_by'] = re.sub(u'(副?議長|議員)', '', response.xpath(u'(//td[re:test(., "^提\s*案\s*人$")]/following-sibling::td)[1]/span/text()').extract_first()).strip().split(u'、')
        item['petitioned_by'] = re.sub(u'(副?議長|議員)', '', (response.xpath(u'(//td[re:test(., "^連\s*署\s*人$")]/following-sibling::td)[1]/span/text()').extract_first() or '')).strip().split(u'、')
        item['motions'] = []
        for motion in [u'審查意見', u'大會決議']:
            resolution = response.xpath(u'(//td[re:test(., "^%s$")]/following-sibling::td)[1]/span/text()' % motion).extract_first()
            if resolution:
                item['motions'].append(dict(zip(['motion', 'resolution', 'date'], [motion, resolution.strip(), None])))
        item['links'] = [
            {
                'url': response.url,
                'note': 'original'
            }
        ]
        for link in response.css('#ctl00_ContentPlaceHolder1_fvDetail_dlRelFile a::attr(href)').extract():
            item['links'].append(
                {
                    'url': urljoin(response.url, link),
                    'note': 'attach'
                }
            )
        return item
