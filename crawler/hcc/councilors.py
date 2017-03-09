# -*- coding: utf-8 -*-
import re
import urllib
from urlparse import urljoin
import scrapy


class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.hcc.gov.tw"]
    start_urls = ["http://www.hcc.gov.tw/2016hcc/member/member.php"]
    download_delay = 0.5

    def parse(self, response):
        links = response.xpath(u'//a[re:test(@href, "skid=\d+$")]/@href').extract()
        for link in links:
            yield scrapy.Request(urljoin(response.url, link), callback=self.parse_profile)

    def parse_profile(self, response):
        item = {}
        item['county'] = u'新竹縣'
        item['election_year'] = '2014'
        item['in_office'] = True
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': '2018-12-24'}
        image_src = response.xpath('//img[@class="media-object"]/@src').extract_first()
        item['image'] = urljoin(response.url, image_src)
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        item['title'], item['name'] = response.xpath('//*[@class="media-major"]/text()').extract_first().split('-')
        region = response.xpath(u'//*[re:test(., "^選舉區別$")]/following-sibling::*[1]/text()').extract_first()
        item['constituency'], item['district'] = re.search(u'([^（]+)（(\S+)）', region).groups()
        item['gender'] = response.xpath(u'//*[re:test(., "性[　\s]*別")]/following-sibling::*[1]/text()').extract_first()
        item['party'] = response.xpath(u'//*[re:test(., "黨[　\s]*籍")]/following-sibling::*[1]/text()').extract_first()
        link = response.xpath(u'//*[re:test(., "個人網站")]/following-sibling::*[1]/descendant::a/@href').extract_first()
        item['links'].append({'url': link, 'note': u'個人網站'})
        mail = response.xpath(u'//*[re:test(., "電子信箱")]/following-sibling::*[1]/descendant::a/@href').re('mailto://(\S+)')
        item['contact_details'] = []
        contact_mappings = {
            u'電話': 'voice',
            u'傳真': 'fax',
            u'通訊地址': 'address',
            u'電子信箱': 'email'
        }
        for label, name in contact_mappings.items():
            values = [x.strip() for x in response.xpath(u'//*[re:test(., "^%s$")]/following-sibling::*[1]/descendant-or-self::*/text()' % u'[　\s]*'.join(label)).extract() if x.strip()]
            for value in values:
                item['contact_details'].append({
                    'label': label,
                    'type': name,
                    'value': value
                })
        item['education'] = [x.strip() for x in response.xpath(u'//*[re:test(., "^學[　\s]*歷$")]/following-sibling::*[1]//text()').extract() if x.strip()]
        item['experience'] = [x.strip() for x in response.xpath(u'//*[re:test(., "^經[　\s]*歷$")]/following-sibling::*[1]//text()').extract() if x.strip()]
        item['platform'] = [x.strip() for x in response.xpath(u'//*[re:test(., "^政[　\s]*見")]/ancestor::div[1]/section//text()').extract() if x.strip()]
        yield item
