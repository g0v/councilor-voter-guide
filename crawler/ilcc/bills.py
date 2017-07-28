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
    allowed_domains = ["ilcc.gov.tw", ]
    start_urls = ["http://www.ilcc.gov.tw"]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    ads = {'1998': 14, '2002': 15, '2005': 16, '2009': 17, '2014': 18, '2018': 19}
    ad = ads[election_year]

    def parse(self, response):
        return response.follow(response.xpath(u'//frame[@name="leftFrame"]/@src').extract_first(), callback=self.parse_tab_frame)

    def parse_tab_frame(self, response):
        return response.follow(response.xpath(u'//a[@title="議案資料庫"]/@href').extract_first(), callback=self.parse_frame)

    def parse_frame(self, response):
        return response.follow(response.xpath(u'//frame[@name="mainFrame"]/@src').extract_first(), callback=self.parse_query)

    def parse_query(self, response):
        yield scrapy.FormRequest.from_response(response, callback=self.parse_list, dont_filter=True)

    def parse_list(self, response):
        for node in response.css('table#dg tr')[1:]:
            item = {}
            item['id'] = re.search(u'Fmotion_instanceOS=([^&]*)', node.xpath('td[1]/descendant::a/@href').extract_first()).group(1)
            yield response.follow(node.xpath('td[1]/descendant::a/@href').extract_first(), callback=self.parse_profile, meta={'item': item})
        next_page = response.xpath(u'//a[re:test(.,"下一頁")]/@href').extract_first()
        has_next_page = response.xpath(u'//select[@name="page"]/option[@selected]/following-sibling::option').extract()
        if next_page and has_next_page:
            payload = {'__EVENTTARGET': re.search("doPostBack\('([^']*)'", next_page).group(1)}
            yield scrapy.FormRequest.from_response(response, formdata=payload, callback=self.parse_list, dont_filter=True, dont_click=True, headers=common.headers(self.county_abbr))

    def parse_profile(self, response):
        item = response.meta['item']
        item_ad = response.css(u'#lbFmotion_expireb::text').extract_first()
        for election_year, ad in self.ads.items():
            if int(item_ad) == ad:
                item['election_year'] = election_year
                break
        if item['election_year'] != self.election_year:
            return
        for key, label in [('bill_id', u'lbFmotion_No'), ('type', u'lbFmotion_Category'), ('category', u'lbFmotion_Class'), ('abstract', u'lbFmotion_From'), ('description', u'lbFmotion_Reason'), ('methods', u'lbFmotion_Way')]:
            content = response.css(u'#%s::text' % label).extract_first()
            if content:
                item[key] = content.strip()
        item['proposed_by'] = re.split(u'\s|、', re.sub(u'(副?議長|議員)', '', response.css(u'#lbFmotion_People::text').extract_first()).strip())
        item['petitioned_by'] = re.split(u'\s|、', re.sub(u'(副?議長|議員)', '', (response.css(u'#lbFmotion_AddTo::text').extract_first() or '')).strip())
        item['motions'] = []
        for motion, label in [(u'大會審議', 'lbFmotion_0'), (u'程序會審定', 'lbFmotion_v'), (u'大會決定', 'lbFmotion_1'), (u'分組審查', 'lbFmotion_g'), (u'大會決議', 'lbFmotion_2')]:
            date = response.css(u'#%sdate::text' % label).extract_first()
            resolution = response.css(u'#%sopinion::text' % label).extract_first()
            if date and resolution:
                item['motions'].append(dict(zip(['motion', 'resolution', 'date'], [motion, resolution.strip(), common.ROC2AD(date)])))
        item['links'] = [
            {
                'url': response.url,
                'note': 'original'
            }
        ]
        return item
