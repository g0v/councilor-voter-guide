# -*- coding: utf-8 -*-
import re
import os
import json
import urllib
from urlparse import urljoin
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from mcc.items import Councilor
from crawler_lib import parse


class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.mcc.gov.tw"]
    start_urls = ["http://www.mcc.gov.tw/imgtxt_list.php?menu=27&typeid=42"]
    download_delay = 0.5

    def __init__(self):
        fh = open(os.path.join(os.path.dirname(__file__), 'constituency.json'), 'r')
        self.constituency = json.loads(fh.read())

    def parse(self, response):
#       response = parse.get_decoded_response(response, 'Big5')
        for node in response.xpath(u'//a[contains(@title, "選區")]'):
            yield Request(urljoin(response.url, node.xpath('@href').extract()[0]), callback=self.parse_profile, meta={'constituency': node.xpath('text()').extract()[0].strip()})

    def parse_profile(self, response):
#       response = parse.get_decoded_response(response, 'Big5')
        items = []
        for name in response.xpath('//table[@id="table98"]/tbody/tr[1]/td/text()').extract():
            item = Councilor()
            item['constituency'] = response.request.meta['constituency']
            item['district'] = self.constituency[item['constituency']]
            item['county'] = u'苗栗縣'
            item['election_year'] = '2009'
            item['term_start'] = '%s-12-25' % item['election_year']
            item['term_end'] = {'date': "2014-12-25"}
            item['in_office'] = True
            item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
            item['name'] = name
            item['image'] = urljoin(response.url, response.xpath(u'//img[@alt="%s"]/@src' % name).extract()[0])
            items.append(item)
        return items
