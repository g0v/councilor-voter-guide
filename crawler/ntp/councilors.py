# -*- coding: utf-8 -*-
import os
import json
import urllib
from urlparse import urljoin

import scrapy


class Spider(scrapy.Spider):
    name = 'councilors'
    start_urls = ["http://www.ntp.gov.tw/content/list/list02.aspx"]

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'constituency.json'), 'r') as infile:
            self.constituency = json.loads(infile.read())

    def parse(self, response):
        for url in response.xpath('//*[@id="main"]/descendant::tr/td[2]/a/@href').extract():
            yield scrapy.Request(urljoin(response.url, url), callback=self.parse_profile)

    def parse_profile(self, response):
        c = {}
        c['image'] = urljoin(
            response.url,
            urllib.quote(response.xpath('//*[@id="main"]/descendant::img[contains(@src, "CouncilorFile")]/@src').extract_first().encode('utf8'))
        )
        c['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        c['constituency'] = response.xpath(u'//*[@id="printContext"]/descendant::a[re:test(text(), "第\d+選區")]/text()').extract_first()
        c['county'] = u'新北市'
        c['election_year'] = '2014'
        c['in_office'] = True
        c['term_start'] = '%s-12-25' % c['election_year']
        c['term_end'] = {'date': '2018-12-24'}
        c['links'] = {'note': u'個人網站', 'url': response.url}
        c['district'] = self.constituency[c['constituency']]
        c['name'] = response.xpath(u'//td[contains(text(), "姓名")]/following-sibling::td[1]/text()').extract_first()
        c['party'] = response.xpath(u'//td[contains(text(), "政黨")]/following-sibling::td[1]/text()').extract_first()
        c['education'] = [x.strip() for x in response.xpath(u'//img[@alt="學歷"]/ancestor::tr[1]/following-sibling::tr[1]/descendant::td/text()').extract() if x.strip()]
        c['experience'] = [x.strip() for x in response.xpath(u'//img[@alt="經歷"]/ancestor::tr[1]/following-sibling::tr[1]/descendant::td/text()').extract() if x.strip()]
        c['title'] = response.xpath(u'//img[@alt="現任"]/ancestor::tr[1]/following-sibling::tr[1]/descendant::td/text()').re(u'(副?議長|議員)')[0]
        c['platform'] = [x.strip() for x in response.xpath(u'//img[@alt="政見"]/ancestor::tr[1]/following-sibling::tr[1]/descendant::td/text()').extract() if x.strip()]
        c['contact_details'] = []
        contact_mappings = {
            u'電話': 'voice',
            u'傳真': 'fax',
            u'通訊處': 'address',
            u'E-mail': 'email'
        }
        for label, name in contact_mappings.items():
            c['contact_details'].append({
                'label': label,
                'type': name,
                'value': response.xpath(u'string(//td[contains(text(), "%s")]/following-sibling::td[1])' % label).extract_first()
            })
        yield c
