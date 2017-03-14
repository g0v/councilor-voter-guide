# -*- coding: utf-8 -*-
import re
import urllib
from urlparse import urljoin
import scrapy


class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.hlcc.gov.tw"]
    start_urls = ["http://www.hlcc.gov.tw/councillor.php", ]
    download_delay = 0.5

    def parse(self, response):
        for node in response.xpath(u'//img[@title="開啟議員個人資料"]'):
            item = {}
            name_text = node.xpath('string(ancestor::span[1])').extract_first().strip()
            item['title'] = re.search(u'(議長|副議長|議員)', name_text).group()
            item['name'] = re.sub(u'(議長|副議長|議員|\s)', '', name_text)
            item['image'] = urljoin(response.url, node.xpath('@src').extract_first())
            constituency = node.xpath(u'ancestor::table/descendant::tr[1]/descendant::td[re:test(., "第\S+選區")]')[-1]
            item['constituency'] = constituency.xpath('string()').extract_first().strip()
            item['district'] = u'、'.join(constituency.xpath('following-sibling::td[1]/descendant::*[string-length(text()) > 0]/text()').extract()).strip()
            link = re.search("MM_openBrWindow\('([^']*)", node.xpath('parent::a/@onclick').extract_first()).group(1)
            yield scrapy.Request(urljoin(response.url, link), callback=self.parse_profile, meta={'item': item})

    def parse_profile(self, response):
        item = response.meta['item']
        item['county'] = u'花蓮縣'
        item['election_year'] = '2014'
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': "2018-12-25"}
        item['in_office'] = True
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        item['gender'] = response.xpath(u'//td[re:test(., "性別")]')[-1].xpath('following-sibling::td[1]/text()').extract_first().strip()
        item['party'] = response.xpath(u'//td[re:test(., "黨籍")]')[-1].xpath('following-sibling::td[1]/text()').extract_first().strip()
        item['contact_details'] = []
        contact_mappings = {
            u'聯絡電話': 'voice',
            u'服務處地址': 'address'
        }
        for label, name in contact_mappings.items():
            values = [x.strip() for x in response.xpath(u'//td[re:test(., "%s")]' % label)[-1].xpath('following-sibling::td[1]/text()').extract() if x.strip()]
            for value in values:
                item['contact_details'].append({
                    'label': label,
                    'type': name,
                    'value': value
                })
        item['education'] = [x.strip() for x in response.xpath(u'//td[re:test(., "學歷")]')[-1].xpath('following-sibling::td[1]/text()').extract() if x.strip()]
        item['experience'] = [x.strip() for x in response.xpath(u'//td[re:test(., "經歷")]')[-1].xpath('following-sibling::td[1]/text()').extract() if x.strip()]
        for key in ['education', 'experience']:
            if len(item[key]) == 1:
                item[key] = item[key][0].split(u'。')
        yield item
