# -*- coding: utf-8 -*-
import re
import urllib
from urlparse import urljoin
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from tycc.items import Councilor
from crawler_lib import parse
from crawler_lib import misc


class Spider(scrapy.Spider):
    name = "councilors"
    start_urls = ["http://www.tycc.gov.tw/page.aspx?wtp=1&wnd=204", ]
    download_delay = 0.5

    def parse(self, response):
        sel = Selector(response)
        urls = sel.xpath('//map/area/@href').extract()
        for url in urls:
            url = urljoin(response.url, url)
            yield Request(url, callback=self.parse_selection_index)

    def parse_selection_index(self, response):
        sel = Selector(response)
        urls = sel.xpath('//div[@id="ctl04_ctl08_pageControl_PN_LIST"]//a/@href').extract()
        for url in urls:
            url = urljoin(response.url, url)
            yield Request(url, callback=self.parse_profile)

    def parse_profile(self, response):
        sel = Selector(response)

        main_node = sel.xpath('//table[@class="specpage_data_table"]//table[2]')
        info_node = main_node.xpath('.//table[2]')
        curr_url = response.url

        item = Councilor()
        item['contact_details'] = []
        item['name'] = \
            info_node.xpath('.//span[@id="ctl04_ctl08_pageControl_LB_MEM_NAME"]/text()').extract()[0].split()[0]
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        img_url = main_node.xpath('.//img[@class="memImg"]/@src').extract()[0]
        item['image'] = urljoin(curr_url, img_url)

        key_map = {
            u'學歷': 'education',
            u'經歷': 'experience'
        }

        county = u'桃園縣'
        rows = info_node.xpath('.//tr')
        is_contact_info = False
        for row in rows:
            key = parse.get_extracted(row.xpath('.//img/@alt'))
            if key == u'聯絡資訊':
                is_contact_info = True
            elif key == u'首頁圖示':
                info = parse.get_inner_text(row).split()
                for group in info:
                    split = group.split(u'：')
                    if len(split) > 1:
                        left, right = split
                        misc.append_contact(item, 'address', left, right)

            td = row.xpath('./td[2]')
            value = parse.get_inner_text(td)
            if not value:
                continue

            k_eng = key_map.get(key)
            if is_contact_info:
                left, right = value.split(u'：')
                url = parse.get_extracted(row.xpath('.//a/@href'))
                if left == 'EMAIL':
                    url = url.lstrip('mailto://')
                    for u in url.split(';'):
                        misc.append_contact(item, 'email', left, u.strip())
                if left == u'聯絡電話':
                    for x in right.split(';'):
                        misc.append_contact(item, 'voice', left, x.strip())
                if left == u'傳真':
                    for x in right.split(';'):
                        misc.append_contact(item, 'fax', left, x.strip())
                if left in [u'部落格', u'FACEBOOK', u'臉書']:
                    item['links'].append({'url': url, 'note': left})
            elif k_eng:
                values = parse.get_inner_text_lines(td)
                values = [parse.remove_whitespaces(v) for v in values]
                item[k_eng] = values
            elif key == u'選區':
                split = value.split()
                item['county'] = county
                item['district'] = split[1] if len(split) > 1 else ''
                item['constituency'] = county + split[0]

        return item

