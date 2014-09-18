# -*- coding: utf-8 -*-
import re
import urllib
from urlparse import urljoin
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from hccc.items import Councilor
from crawler_lib import parse
from crawler_lib import misc


class Spider(scrapy.Spider):
    name = "councilors"
    base_url = "http://www.hsinchu-cc.gov.tw"
    allowed_domains = ["www.hsinchu-cc.gov.tw"]
    start_urls = ["http://www.hsinchu-cc.gov.tw/content/councilor.htm", ]
    download_delay = 0.5

    def parse(self, response):
        sel = Selector(response)
        nodes = sel.xpath(u'//a')
        base_url = self.base_url + '/content/'
        for node in nodes:
            url = base_url + node.xpath('@href').extract()[0]
            yield Request(url, callback=self.parse_profile)

    def parse_profile(self, response):
        sel = Selector(response)
        main_node = sel.xpath('/html/body/table/tbody/tr[1]/td/table[2]/tbody')
        basic_info_node = main_node.xpath('tr[1]/td[2]/p')
        sub_table_node = main_node.xpath('.//tbody')
        base_url = self.base_url + '/content/'

        item = Councilor()
        item['contact_details'] = []
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        item['image'] = base_url + parse.get_extracted(sel.xpath(u'//div/img/@src'))

        key_map = {
            u'性別': 'gender',
            u'黨籍': 'party',
            u'選區': 'constituency',
        }

        for i, line in enumerate(basic_info_node.xpath('.//text()').extract()):
            line = line.strip()
            if i == 0:
                item['name'] = line
                continue

            cols = line.split(u'：')
            k_chinese = parse.remove_whitespaces(cols[0])
            value = cols[1]

            k_eng = key_map.get(k_chinese)
            if k_eng:
                item[k_eng] = value

        for tr in sub_table_node.xpath('tr'):
            cols = tr.xpath('td')
            left = parse.remove_whitespaces(parse.get_extracted(cols[0].xpath('text()')).strip())
            right = parse.get_inner_text(cols[1])

            if left == u'政見':
                item['platform'] = parse.get_inner_text_lines(cols[1])
            if left == u'服務處地址':
                misc.append_contact(item, 'address', left, right)
            if left == u'電子郵件信箱':
                misc.append_contact(item, 'email', left, right)
            if u'電話' in left:
                misc.append_contact(item, 'voice', left, right)
            if u'網址' in left:
                item['links'].append({'url': right, 'note': left})

        return item

