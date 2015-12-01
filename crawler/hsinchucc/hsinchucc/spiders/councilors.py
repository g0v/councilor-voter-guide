# -*- coding: utf-8 -*-
import re
import urllib
from urlparse import urljoin
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from hsinchucc.items import Councilor


class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.hsinchu-cc.gov.tw"]
    start_urls = ["http://www.hsinchu-cc.gov.tw/content/Councilor.htm",]
    download_delay = 0.5

    def parse(self, response):
        sel = Selector(response)
        nodes = sel.xpath('//a[contains(@href, ".htm")]')
        for node in nodes:
            item = Councilor()
            item['election_year'] = '2009'
            item['county'] = '新竹市'
            item['in_office'] = True
            item['term_start'] = '%s-12-25' % item['election_year']
            item['term_end'] = {'date': '2014-12-25'}
            item['contact_details'] = []
            item['name'] = node.xpath('text()').extract()[0].strip()
            title = node.xpath('../text()').re(u'(\S+)：')
            item['title'] = title[0] if title else u'議員'
            yield Request(urljoin(self.start_urls[0], node.xpath('@href').extract()[0]), callback=self.parse_profile, meta={'item': item})

    def parse_profile(self, response):
        sel = Selector(response)
        item = response.meta['item']
        image = sel.xpath(u'//img[contains(@src, "image")]/@src').extract()[-1]
        item['image'] = urljoin(response.url, urllib.quote(image.encode('utf8')))
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        item['gender'] = sel.xpath('//text()').re(u'性\s*別：(\S+)')[0]
        item['party'] = sel.xpath('//text()').re(u'黨\s*籍：(\S+)')[0]
        item['district'] = sel.xpath('//text()').re(u'選\s*區：(\S+)')[0]
        maps = {
            u'服務處地址': 'address',
            u'服務電話': 'voice',
            u'行動電話': 'cell',
            u'傳真': 'fax',
            u'電子郵件': 'email'
        }
        for tr in sel.xpath('//tr'):
            tds = tr.xpath('td')
            text = ''.join([re.sub('[ \s]', '', x) for x in tds[0].xpath('descendant::text()').extract()])
            for k, v in maps.iteritems():
                if k == text:
                    item['contact_details'].append({'type': v, 'label': k, 'value': ''.join([re.sub('[ \s]', '', x) for x in tds[1].xpath('descendant::text()').extract()])})
                    break
            if text == u'政見':
                item['platform'] = [x.strip() for x in tds[1].xpath('descendant::text()').extract() if x.strip()]
        return item
