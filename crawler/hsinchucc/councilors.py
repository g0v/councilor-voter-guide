# -*- coding: utf-8 -*-
import re
import urllib
from urlparse import urljoin
import scrapy


class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.hsinchu-cc.gov.tw"]
    start_urls = ["http://www.hsinchu-cc.gov.tw/content/Councilor.htm",]
    download_delay = 0.5

    def parse(self, response):
        nodes = response.xpath('//a[contains(@href, ".htm")]')
        for node in nodes:
            item = {}
            item['election_year'] = '2014'
            item['county'] = u'新竹市'
            item['in_office'] = True
            item['term_start'] = '%s-12-25' % item['election_year']
            item['term_end'] = {'date': '2018-12-25'}
            item['contact_details'] = []
            item['name'] = node.xpath('string()').extract_first().strip()
            title = node.xpath('preceding::font[1]/text()').re(u'(\S+)：')
            item['title'] = title[0] if title else u'議員'
            yield scrapy.Request(urljoin(self.start_urls[0], node.xpath('@href').extract_first()), callback=self.parse_profile, meta={'item': item})

    def parse_profile(self, response):
        item = response.meta['item']
        image = response.xpath(u'//img[re:test(@src, "^image/")]/@src').extract()[-1]
        item['image'] = urljoin(response.url, urllib.quote(image.encode('utf8')))
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        lines = response.xpath('//text()').extract()
        for i, line in enumerate(lines):
            if re.search(u'性\s*別：(\S+)', line):
                item['gender'] = re.search(u'性\s*別：(\S+)', line).group(1)
            elif re.search(u'性\s*別：', line):
                item['gender'] = lines[i+1]
            if re.search(u'黨\s*籍：(\S+)', line):
                item['party'] = re.search(u'黨\s*籍：(\S+)', line).group(1)
            elif re.search(u'黨\s*籍：', line):
                item['party'] = lines[i+1]
            if re.search(u'選\s*區：(\S+)', line):
                item['district'] = re.search(u'選\s*區：(\S+)', line).group(1)
            elif re.search(u'選\s*區：', line):
                item['district'] = lines[i+1]
            if item.get('gender') and item.get('party') and item.get('district'):
                break
        contact_mappings = {
            u'服務處地址': 'address',
            u'服務電話': 'voice',
            u'行動電話': 'cell',
            u'傳真': 'fax',
            u'電子郵件': 'email'
        }
        for label, name in contact_mappings.items():
            values = [x.strip() for x in response.xpath(u'//td[re:test(., "%s")]/following-sibling::td[1]/descendant-or-self::*/text()' % '\s*'.join(label)).extract() if x.strip()]
            for value in values:
                item['contact_details'].append({
                    'label': label,
                    'type': name,
                    'value': value
                })
        for label in [u'個人網站', u'部落格網址']:
            nodes = response.xpath(u'//td[re:test(., "%s")]/following-sibling::td[1]/descendant::a/@href' % '\s*'.join(label)).extract()
            for node in nodes:
                item['links'].append({
                    'url': node,
                    'note': label
                })
        item['platform'] = []
        item['platform'].append(''.join([x.strip() for x in response.xpath(u'//td[re:test(., "政\s*見")]/following-sibling::td/text()').extract()]))
        for tr in response.xpath(u'//td[re:test(., "政\s*見")]/parent::tr[1]/preceding-sibling::tr[1]/following-sibling::tr[position() > 1]'):
            line = tr.xpath('normalize-space(string())').extract_first().strip()
            if line:
                item['platform'].append(line)
        return item
