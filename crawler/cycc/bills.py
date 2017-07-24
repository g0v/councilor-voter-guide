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
    allowed_domains = ["cycc.gov.tw", ]
    start_urls = ["http://www.cycc.gov.tw/index2.asp"]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    ads = {'2009': 17, '2014': 18, '2018': 19}
    ad = ads[election_year]

    def parse(self, response):
        return response.follow(response.xpath(u'//a[img[@alt="議案查詢"]]/@href').extract_first(), callback=self.parse_tab)

    def parse_tab(self, response):
        return response.follow(response.xpath(u'//a[re:test(., "^議決案檢索$")]/@href').extract_first(), callback=self.parse_query)

    def parse_query(self, response):
        for value in response.xpath(u'//select[@name="sid"]/option/@value').extract():
            payload = {'sid': value}
            yield scrapy.FormRequest.from_response(response, formdata=payload, callback=self.parse_list, dont_filter=True, dont_click=True, headers=common.headers(self.county_abbr))

    def parse_list(self, response):
        for i, node in enumerate(response.xpath('//table[@bgcolor][not(caption)]')):
            item = {}
            item['election_year'] = self.election_year
            item['id'] = '%s-%02d' % ('-'.join(re.sub('\D', ' ', response.url).split()), i)
            for key, label in [('category', u'類[\s　]*別'), ('abstract', u'案[\s　]*由'), ('description', u'理[\s　]*由'), ('methods', u'辦[\s　]*法'), ('', u''), ]:
                    content = response.xpath(u'(//*[re:test(., "%s")]/following-sibling::td)[1]/span/text()' % label).extract_first()
                    if content:
                        item[key] = content.strip()
            item['proposed_by'] = re.sub(u'(副?議長|議員)', '', response.xpath(u'(//*[re:test(., "提[\s　]*案[\s　]*人")]/following-sibling::td)[1]/span/text()').extract_first()).strip().split(u'、')
            item['petitioned_by'] = re.sub(u'(副?議長|議員)', '', (response.xpath(u'(//*[re:test(., "連[\s　]*署[\s　]*人")]/following-sibling::td)[1]/span/text()').extract_first() or '')).strip().split(u'、')
            item['motions'] = []
            for motion in [u'審查意見', u'決議']:
                resolution = response.xpath(u'(//*[re:test(., "%s")]/following-sibling::td)[1]/span/text()' % u'[\s　]*'.join(motion)).extract_first()
                if resolution:
                    item['motions'].append(dict(zip(['motion', 'resolution', 'date'], [motion, resolution.strip(), None])))
            item['links'] = [
                {
                    'url': response.url,
                    'note': 'original'
                }
            ]
            yield item
        next_page = response.xpath(u'//a[img[@alt="下一頁"]]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse_list)
