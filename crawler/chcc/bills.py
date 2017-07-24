# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
import urllib
import scrapy

import common


class Spider(scrapy.Spider):
    name = "bills"
    allowed_domains = ["chcc.gov.tw", ]
    start_urls = ["http://www.chcc.gov.tw"]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    ads = {'2005': u'十六', '2009': u'十七', '2014': u'十八', '2018': u'十九'}
    ad = ads[election_year]

    def parse(self, response):
        return response.follow(response.css('li:not(.dropdown)').xpath(u'a[re:test(., "^議案審查$")]/@href').extract_first(), callback=self.parse_query)

    def parse_query(self, response):
        iid = response.xpath(u'//select[@name="iid"]/option[re:test(., "%s屆")]/@value' % self.ad).extract_first()
        payload = {'iid': iid}
        return scrapy.FormRequest.from_response(response, formcss='#council2_type3 form', formdata=payload, callback=self.parse_result, dont_filter=True)

    def parse_result(self, response):
        for link in response.css('#council2 li:not(:first-child) a::attr(href)').extract():
            yield response.follow(link, callback=self.parse_list)
        next_page = response.xpath(u'//a[img/@alt="下一頁"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse_result)

    def parse_list(self, response):
        for node in response.css('#council2 li:not(:first-child)'):
            item = {}
            item['election_year'] = self.election_year
            item['execution'] = node.xpath('div[4]/descendant-or-self::*/text()').extract_first()
            yield response.follow(node.xpath('div[6]/a/@href').extract_first(), callback=self.parse_profile, meta={'item': item})
        next_page = response.xpath(u'//a[img/@alt="下一頁"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse_list)

    def parse_profile(self, response):
        item = response.meta['item']
        item['id'] = '-'.join(re.sub('\D', ' ', response.url.split('=')[-1]).split())
        item['type'] = response.xpath('//*[@id="council2_title"]/span/text()').extract_first().split()[-1]
        for key, label in [('category', u'類別'), ('abstract', u'案由'), ('description', u'說明'), ('methods', u'辦法'), ('', u''), ]:
            content = response.xpath(u'(//div[re:test(., "^%s$")]/following-sibling::div)[1]/text()' % label).extract_first()
            if content:
                item[key] = content.strip()
        item['proposed_by'] = response.xpath(u'(//div[re:test(., "^提案人$")]/following-sibling::div)[1]/text()').extract_first().strip().split(u'、')
        item['petitioned_by'] = (response.xpath(u'(//div[re:test(., "^(連署|附議)人$")]/following-sibling::div)[1]/text()').extract_first() or '').strip().split(u'、')
        item['motions'] = []
        for motion in [u'審查意見', u'大會決議']:
            resolution = response.xpath(u'(//div[re:test(., "^%s$")]/following-sibling::div)[1]/text()' % motion).extract_first()
            if resolution:
                item['motions'].append(dict(zip(['motion', 'resolution', 'date'], [motion, resolution.strip(), None])))
        item['links'] = [
            {
                'url': response.url,
                'note': 'original'
            }
        ]
        return item
