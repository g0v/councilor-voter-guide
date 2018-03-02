# -*- coding: utf-8 -*-
import re
import urllib
from urlparse import urljoin
import scrapy


class Spider(scrapy.Spider):
    name = "councilors_constituencies"
    allowed_domains = ["db.cec.gov.tw"]
    start_urls = ["http://db.cec.gov.tw/",]
    download_delay = 1

    def parse(self, response):
        for level in response.xpath(u'//a[re:test(., "^2014.+議員選舉$")]/@href').extract():
            yield response.follow(level, callback=self.parse_level)

    def parse_level(self, response):
        ref = {
            u'區域': {'constituency_type_title': u'區域', 'constituency_type': 'regional'},
            u'平原': {'constituency_type_title': u'平地原住民', 'constituency_type': 'ethnical'},
            u'山原': {'constituency_type_title': u'山地原住民', 'constituency_type': 'ethnical'},
            u'不分區政黨': {'constituency_type_title': u'全國不分區', 'constituency_type': 'PR'},
        }
        for region in response.xpath(u'//div[re:test(., "候選人得票明細")]/following-sibling::div/a'):
            yield response.follow(region.xpath('@href').extract_first(), callback=self.parse_region, meta={'meta': ref[region.xpath('text()').extract_first().strip()]})

    def parse_region(self, response):
        m = response.meta['meta']
        for constituency in response.css(u'table.ctks tr.data td[rowspan] a'):
            constituency_label = constituency.xpath('text()').extract_first()
            m['constituency_label'] = constituency_label
            yield response.follow(constituency, callback=self.parse_constituency, meta={'meta': m})

    def parse_constituency(self, response):
        d = response.meta['meta']
        constituency_label = response.meta['meta']['constituency_label']
        print(constituency_label)
        county = re.sub(u'第\d+.+', '', constituency_label)
        constituency_number = int(re.sub('\D', '', constituency_label))
        print(county, constituency_number)
        d.update({
            'constituency_label_wiki': u'%s議員第%d選舉區' % (county, constituency_number),
            'constituency_label': constituency_label,
            'county': county,
            'constituency_number': constituency_number,
            'districts': [],
        })
        for town in response.css(u'table.ctks tr.data td[rowspan] a'):
            print(town.xpath('text()').extract_first())
            town_label = re.sub(u'.+?選區', '', town.xpath('text()').extract_first())
            print(town_label)
            d['districts'].append(town_label)
        return d
