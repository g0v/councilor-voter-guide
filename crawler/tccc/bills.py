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
    allowed_domains = ["tccc.gov.tw", ]
    start_urls = ["http://www.tccc.gov.tw/"]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    ads = {'2010': 1, '2014': 2, '2018': 3}
    ad = ads[election_year]

    def parse(self, response):
        return response.follow(response.xpath(u'//a[re:test(., "^議會連結$")]/@href').extract_first(), callback=self.parse_frame)

    def parse_frame(self, response):
        return response.follow(response.xpath(u'//iframe[@name="wb_main"]/@src').extract_first(), callback=self.parse_tab)

    def parse_tab(self, response):
        return response.follow(response.xpath(u'//a[re:test(., "議案查詢$")]/@href').extract_first(), callback=self.parse_meta_refresh, meta={'dont_redirect': True})

    def parse_meta_refresh(self, response):
        fixed_url = response.xpath('//meta[@http-equiv="refresh"]/@content').re('url=(.*)')[0].replace('\\', '/').lstrip('../')
        return response.follow(fixed_url, callback=self.parse_login)

    def parse_login(self, response):
        payload = dict(zip(['account', 'pw'], response.xpath('//text()').re(u'帳號:(\S*)  密碼:(\S*)')))
        return scrapy.FormRequest.from_response(response, formname='form1', formdata=payload, callback=self.parse_logined)

    def parse_logined(self, response):
        for link in response.xpath(u'//a[re:test(., "提案查詢$")]/@href'):
            yield response.follow(link, callback=self.parse_query, meta={'dont_redirect': True})

    def parse_query(self, response):
        for value in response.xpath(u'//select[@name="SPeriod"]/optgroup[re:test(., "%s屆")]/option/@value' % self.ad).extract():
            payload = {'SPeriod': value}
            yield scrapy.FormRequest.from_response(response, formname='form1', formdata=payload, callback=self.parse_list)

    def parse_list(self, response):
        for node in response.xpath('//*[count(td)=11][position()>1]'):
            item = {}
            item['election_year'] = self.election_year
            item['id'] = node.xpath('td[1]/input/@value').extract_first()
            item['category'] = node.xpath('td[3]/text()').extract_first().split('-')[-1].strip()
            item['type'] = re.sub('\s', '', node.xpath('td[4]/text()').extract_first())
            item['proposed_by'] = node.xpath('td[5]/text()').extract_first().strip().split(u'、')
            item['petitioned_by'] = node.xpath('td[6]/text()').extract_first().strip().split(u'、') if node.xpath('td[6]/text()').extract_first() else []
            item['bill_no'] = re.sub('\s', '', node.xpath('td[7]/text()').extract_first())
            item['abstract'] = node.xpath('td[8]/descendant-or-self::*/text()').extract_first()
            item['execution'] = re.sub('\s', '', node.xpath('td[10]/text()').extract_first())
            link = urljoin(response.url, 'html_e_print.php?id=%s' % item['id'])
            yield response.follow(link, callback=self.parse_profile, meta={'item': item})
        next_page = response.xpath(u'//a[re:test(., "下一頁")]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse_list)

    def parse_profile(self, response):
        item = response.meta['item']
        item['description'] = response.xpath(u'//td[re:test(., "理[\s　]*由")]/following-sibling::td/descendant-or-self::*/text()').extract_first()
        item['methods'] = response.xpath(u'//td[re:test(., "辦[\s　]*法")]/following-sibling::td/descendant-or-self::*/text()').extract_first()
        item['motions'] = []
        for motion in [u'審查意見', u'大會議決']:
            resolution = response.xpath(u'//td[re:test(., "%s")]/following-sibling::td/descendant-or-self::*/text()' % u'[\s　]*'.join(motion)).extract_first()
            if resolution:
                item['motions'].append(dict(zip(['motion', 'resolution', 'date'], [motion, resolution, None])))
        item['links'] = [
            {
                'url': response.url,
                'note': 'original'
            },
        ]
        yield item
