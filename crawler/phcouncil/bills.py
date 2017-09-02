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
    allowed_domains = ["phcouncil.gov.tw", ]
    start_urls = ["http://www.phcouncil.gov.tw/"]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = '2009'
#   election_year = common.election_year(county_abbr)
    ads = {'2009': 17, '2014': 18, '2018': 19}
    ad = ads[election_year]

    def parse(self, response):
        for node in response.xpath(u'((//a[re:test(., "^議會相關法案$")]/following-sibling::ul)[1]/descendant::*[re:test(., "第\s*%s\s*屆")]/following-sibling::ul)[1]/descendant::a' % self.ad):
            yield response.follow(node.xpath('@href').extract_first(), callback=self.parse_query, meta={'type': node.xpath('text()').extract_first()})

    def parse_query(self, response):
        for link in response.css(u'#Main_Table').xpath(u'descendant::a[re:test(., "詳細內容")]/@href').extract():
            yield response.follow(link, callback=self.parse_list, meta={'type': response.meta['type']})
        next_page = response.xpath(u'//a[img[@alt="下一頁"]]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse_query, meta={'type': response.meta['type']})

    def parse_list(self, response):
        for link in response.css(u'#Main_Table').xpath(u'descendant::a[re:test(., "詳細內容")]/@href').extract():
            yield response.follow(link, callback=self.parse_profile, meta={'type': response.meta['type']})
        next_page = response.xpath(u'//a[img[@alt="下一頁"]]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse_list, meta={'type': response.meta['type']})

    def parse_profile(self, response):
        item = {}
        item['election_year'] = self.election_year
        item['type'] = response.meta['type']
        item['id'] = re.search(u'id=([^&]*)', response.url).group(1)
        for key, label in [('category', u'類[\s　]*別'), ('abstract', u'案[\s　]*由'), ('description', u'說[\s　]*明'), ('methods', u'辦[\s　]*法'), ('execution', u'決[\s　]*議')]:
                content = response.xpath(u'string((//*[re:test(., "%s")]/following-sibling::td)[1])' % label).extract_first()
                if content:
                    item[key] = content.strip()
        if item['type'] == u'縣府提案':
            item['proposed_by'] = u'縣府'
        else:
            item['proposed_by'] = re.split(u'[，、 ]', re.sub(u'(副?議長|議員)', '', response.xpath(u'(//*[re:test(., "(提[\s　]*案|動[\s　]*議|請[\s　]*願)[\s　]*人")]/following-sibling::td)[1]/text()').extract_first()).strip())
        item['petitioned_by'] = re.split(u'[，、 ]', re.sub(u'(副?議長|議員)', '', (response.xpath(u'(//*[re:test(., "(連[\s　]*署|附[\s　]*議)[\s　]*人")]/following-sibling::td)[1]/text()').extract_first() or '')).strip())
        item['links'] = [
            {
                'url': response.url,
                'note': 'original'
            }
        ]
        yield item
