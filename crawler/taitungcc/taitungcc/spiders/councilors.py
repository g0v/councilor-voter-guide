# -*- coding: utf-8 -*-
import re
import os
import json
import urllib
from urlparse import urljoin
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from taitungcc.items import Councilor


class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.taitungcc.gov.tw"]
    start_urls = ["http://www.taitungcc.gov.tw/ourteam/%02dourteam.html" % x for x in range(2, 16)]
    download_delay = 0.5

    def __init__(self):
        fh = open(os.path.join(os.path.dirname(__file__), 'constituency.json'), 'r')
        self.constituency = json.loads(fh.read())

    def parse(self, response):
        for node in response.xpath('//td[@class="ourteam01"]/a'):
            item = Councilor()
            item['name'] = node.xpath('text()').extract()[0]
            item['constituency'] = u'第%d選區' % (int(re.search('(\d+)ourteam', response.url).group(1))-1)
            item['district'] = self.constituency[item['constituency']]
            yield Request(urljoin(response.url, node.xpath('@href').extract()[0]), callback=self.parse_profile, meta={'item': item})

    def parse_profile(self, response):
        item = response.request.meta['item']
        item['county'] = u'臺東縣'
        item['election_year'] = '2009'
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': "2014-12-25"}
        item['in_office'] = True
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        item['image'] = urljoin(response.url, response.xpath('//td[@background="images/page02_pic02_013.jpg"]/img/@src').extract()[0])
        item['contact_details'] = []
        for x in response.xpath('//img[contains(@src, "page05_pic02_002.jpg")]'):
            label = ''.join([y.strip() for y in x.xpath('../descendant::text()').extract()])
            value = x.xpath('../following-sibling::td[1]/descendant::text()').extract()
            if value:
                if re.search(u'性別', label):
                    item['gender'] = value[0]
                elif re.search(u'黨籍', label):
                    item['party'] = value[0]
                elif re.search(u'電話', label):
                    item['contact_details'].append({"label" : u'電話', "type" : "voice", "value" : value[0]})
                elif re.search(u'傳真', label):
                    item['contact_details'].append({"label" : u'傳真', "type" : "fax", "value" : value[0]})
                elif re.search(u'地址', label):
                    item['contact_details'].append({"label" : u'地址', "type" : "address", "value" : value[0]})
                elif re.search(u'E-mail', label):
                    item['contact_details'].append({"label" : u'E-mail', "type" : "email", "value" : value[0]})
        for td in response.xpath(u'//td//strong'):
            label = td.xpath('text()').extract()[0].strip()
            value = [line.strip() for line in td.xpath('ancestor::td/text()').extract()]
            if re.search(u'學歷', label):
                item['education'] = value
            elif re.search(u'經歷', label):
                item['experience'] = value
            elif re.search(u'政見', label):
                item['platform'] = value
        return item
