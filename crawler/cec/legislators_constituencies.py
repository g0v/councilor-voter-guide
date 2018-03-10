# -*- coding: utf-8 -*-
import os
import re
import json
import urllib
from urlparse import urljoin
import scrapy


class Spider(scrapy.Spider):
    name = "councilors_constituencies"
    allowed_domains = ["db.cec.gov.tw"]
    start_urls = ["http://db.cec.gov.tw/",]
    download_delay = 1
    num_ref = [u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'十', u'十一', u'十二', u'十三', u'十四', u'十五', u'十六', u'十七', u'十八', u'十九']

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), '../../data/cec/national_constituencies_from_wikidata.json'), 'r') as infile:
            self.ref = json.loads(infile.read())

    def parse(self, response):
        for level in response.xpath(u'//a[re:test(., "^2016.+立法委員選舉$")]/@href').extract():
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
        for constituency in response.css(u'table.ctks tr.data td[rowspan] a'):
            yield response.follow(constituency.xpath('@href').extract_first(), callback=self.parse_constituency, meta={'meta': response.meta['meta']})

    def parse_constituency(self, response):
        for town in response.css(u'table.ctks tr.data td[rowspan] a'):
            yield response.follow(town.xpath('@href').extract_first(), callback=self.parse_villages, meta={'meta': response.meta['meta']})

    def parse_villages(self, response):
        m = re.search(u'(?P<county>.+?[縣市])第(?P<constituency_number>\d+)選區(?P<district>.+?[鄉鎮市區])(?P<villages>.+)', response.css(u'table.ctks tr.data td[rowspan] a').xpath('text()').extract_first())
        county = m.group('county')
        constituency_number = int(m.group('constituency_number'))
        print(county, constituency_number)
        d = {
            'constituency_type_title': response.meta['meta']['constituency_type_title'],
            'constituency_type': response.meta['meta']['constituency_type'],
            'constituency_label_wiki': u'%s第%s選舉區' % (county, self.num_ref[constituency_number-1]),
            'constituency_label': u'%s第%02d選區' % (county, constituency_number),
            'county': county,
            'constituency_number': constituency_number,
            'district': m.group('district'),
            'villages': [],
        }
        for r in self.ref:
            if r['itemLabel'] == d['constituency_label_wiki']:
                d['wikidata_item'] = r['item']
                break
        for village in response.css(u'table.ctks tr.data td[rowspan] a'):
            villages_label = re.sub(u'.+?選區.+?[鄉鎮市區]', '', village.xpath('text()').extract_first())
            print(villages_label)
            d['villages'].extend(villages_label.split(u'、'))
        return d
