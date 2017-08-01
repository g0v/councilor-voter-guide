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
    allowed_domains = ["taitungcc.gov.tw", ]
    start_urls = ["http://www.taitungcc.gov.tw"]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    ads = {'2009': 17, '2014': 18, '2018': 19}
    ad = ads[election_year]

    def parse(self, response):
        return response.follow(response.xpath(u'//a[re:test(., "^議案查詢$")]/@href').extract_first(), callback=self.parse_list)

    def parse_list(self, response):
        pages = response.css('#BodyContent_PageHelpWuc1_lbTotalInFo::text').extract_first()
        print pages
        for node in response.css('table.list3 tbody tr'):
            node_ad = int(node.xpath('td[1]/text()').re(u'(\d+)\s*屆')[0])
            if node_ad < self.ad:
                break
            if node_ad > self.ad:
                continue
            yield response.follow(node.xpath('@onclick').re("href='(.*)'")[0], callback=self.parse_profile)
        next_page = response.xpath(u'//input[re:test(@value, "下一頁")][not(@disabled)]')
        if next_page:
            payload = {next_page.xpath('@name').extract_first(): next_page.xpath('@value').extract_first()}
            yield scrapy.FormRequest.from_response(response, formdata=payload, callback=self.parse_list, dont_filter=True, dont_click=True, headers=common.headers(self.county_abbr))

    def parse_profile(self, response):
        item = {}
        item['election_year'] = self.election_year
        item['id'] = re.search('=([^&]*)', response.url).group(1).zfill(6)
        item['bill_id'] = response.xpath(u'(//td[re:test(., "^案[\s　]*號$")]/following-sibling::td)[1]/text()').extract_first()
        item['category'] = re.search(u'.*?類', response.xpath(u'(//td[re:test(., "^案[\s　]*號$")]/following-sibling::td)[1]/text()').extract_first()).group(0)
        for key, label in [('type', u'議案分類'), ('abstract', u'案由'), ('description', u'說明'), ('methods', u'辦法')]:
                content = response.xpath(u'(//td[re:test(., "^%s$")]/following-sibling::td)[1]/text()' % label).extract_first()
                if content:
                    item[key] = content.strip()
        item['proposed_by'] = re.sub(u'(副?議長|議員)', '', response.xpath(u'(//td[re:test(., "^(動議|提案|請願)(單位|人)(姓名)?$")]/following-sibling::td)[1]/text()').extract_first()).strip().split(u'、')
        item['petitioned_by'] = re.sub(u'(副?議長|議員)', '', (response.xpath(u'(//td[re:test(., "^(連署|附議)人$")]/following-sibling::td)[1]/text()').extract_first() or '')).strip().split(u'、')
        item['motions'] = []
        for motion in [u'審查意見', u'大會決議']:
            resolution = response.xpath(u'(//td[re:test(., "^%s$")]/following-sibling::td)[1]/text()' % motion).extract_first()
            if resolution:
                item['motions'].append(dict(zip(['motion', 'resolution', 'date'], [motion, resolution.strip(), None])))
        item['links'] = [
            {
                'url': response.url,
                'note': 'original'
            }
        ]
        return item
