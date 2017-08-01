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
    allowed_domains = ["tncc.gov.tw", ]
    start_urls = ["http://www.tncc.gov.tw"]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    ads = {'2010': 1, '2014': 2, '2018': 3}
    ad = ads[election_year]

    def parse(self, response):
        return response.follow(response.xpath(u'//a[re:test(., "^議案資訊$")]/@href').extract_first(), callback=self.parse_query)

    def parse_query(self, response):
        for value in response.xpath(u'//select[@name="motiondept"]/option[not(@value="")]/@value').extract():
            payload = {
                'menu1': response.xpath(u'//select[@name="menu1"]/option[re:test(., "第\s*%d\s*屆")]/@value' % self.ad).extract_first(),
                'motiondept': value
            }
            yield scrapy.FormRequest.from_response(response, formdata=payload, callback=self.parse_list, dont_filter=True, dont_click=True, headers=common.headers(self.county_abbr))

    def parse_list(self, response):
        for link in response.xpath('//table[@id="printa"]/descendant::tr[count(td)>1]/descendant::a/@href'):
            yield response.follow(link, callback=self.parse_profile)
        next_page = response.xpath(u'//a[re:test(., "^下一頁$")]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse_list)

    def parse_profile(self, response):
        item = {}
        item['election_year'] = self.election_year
        item['id'] = re.search('=([^&]+)', response.url).group(1)
        for key, label in [('type', u'提案類別'), ('category', u'審查會別'), ('abstract', u'主旨'), ('description', u'說明'), ('methods', u'辦法'), ('execution', u'辦理情形')]:

            content = response.xpath(u'string((//*[re:test(., "^%s$")]/following-sibling::td)[1])' % label).extract_first()
            if content:
                item[key] = content.strip()
        item['proposed_by'] = re.sub(u'(副?議長|議員)', '', response.xpath(u'(//*[re:test(., "^提案單位/人$")]/following-sibling::td)[1]/text()').extract_first()).strip().split(u'、')
        item['petitioned_by'] = re.sub(u'(副?議長|議員)', '', (response.xpath(u'(//*[re:test(., "^連署人$")]/following-sibling::td)[1]/text()').extract_first() or '')).strip().split(u'、')
        item['motions'] = []
        for date, motion in [(u'來文日期', u'來文字號'), (None, u'審查意見'), (u'決議日期', u'大會決議'), (u'發文日期', u'發文字號'), ]:
            date = response.xpath(u'(//*[re:test(., "%s")]/following-sibling::td)[1]/text()' % u'[\s　]*'.join(date)).extract_first() if date else None
            resolution = response.xpath(u'(//*[re:test(., "%s")]/following-sibling::td)[1]/text()' % u'[\s　]*'.join(motion)).extract_first()
            if resolution:
                item['motions'].append(dict(zip(['motion', 'resolution', 'date'], [motion, resolution.strip(), date])))
        item['links'] = [
            {
                'url': response.url,
                'note': 'original'
            }
        ]
        for link in response.xpath(u'(//*[re:test(., "^議會附件")]/following-sibling::td)[1]/descendant::a/@href').extract():
            item['links'].append(
                {
                    'url': urljoin(response.url, link),
                    'note': 'attach'
                }
            )
        yield item
