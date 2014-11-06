# -*- coding: utf-8 -*-
import re
import urllib
from urlparse import urljoin
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from ilcc.items import Councilor
from scrapy.utils.url import canonicalize_url
from crawler_lib import parse
from crawler_lib import misc


class Spider(scrapy.Spider):
    name = "councilors"
    start_urls = ["http://www.ilcc.gov.tw/Html/H_05/H_05.asp", ]
    download_delay = 0.5

    def parse(self, response):
        response = parse.get_decoded_response(response, 'Big5')
        sel = Selector(response)
        areas = sel.xpath(u'//table[contains(@summary,"議員列表")]')
        curr_url = response.url

        for area in areas:
            name = area.xpath('@summary').extract()[0]
            m = re.match('(.*)\((.*)\).*', name)
            area_info = m.groups()

            urls = area.xpath('.//a/@href').extract()

            for i, url in enumerate(urls):
                url = url.encode('Big5')
                url = urljoin(curr_url, url)

                meta = {'area': area_info}

                # manually do the request, because the actual content of H0052.aspx is determined by the session
                res = misc.get_response(url, meta=meta)
                yield self.parse_profile_frameset(res)

    def parse_profile_frameset(self, response):
        sel = Selector(response)

        url = parse.get_extracted(sel.xpath('//frame[@name="mainFrame"]/@src'))
        url = urljoin(response.url, url)
        meta = response.request.meta
        return Request(url, callback=self.parse_profile, meta=meta)

    def parse_profile(self, response):
        response = parse.get_decoded_response(response, 'Big5')
        meta = response.request.meta
        sel = Selector(response)
        curr_url = response.url
        county = u'宜蘭縣'

        tables = sel.xpath('//table[@bgcolor="#333333"]')

        item = Councilor()
        item['contact_details'] = []
        item['county'] = county
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        img_url = sel.xpath('.//div[@id="Layer2"]/img/@src').extract()[0]
        item['image'] = urljoin(curr_url, img_url)

        if meta:
            area = meta['area']
            item['constituency'] = county + area[0]
            item['district'] = area[1]

        key_map = {
            u'黨籍': 'party',
            u'姓名': 'name'
        }
        tds = tables[0].xpath('.//td')
        pairs = [(tds[2 * i], tds[2 * i + 1]) for i in range(len(tds) / 2)]
        for k, v in pairs:
            key = parse.get_inner_text(k, remove_white=True)
            value = parse.get_inner_text(v).strip()

            k_eng = key_map.get(key)
            if k_eng:
                item[k_eng] = value
            elif key == 'E-mail':
                if value:
                    misc.append_contact(item, 'email', key, value)
            elif u'電話' in key:
                misc.append_contact_list(item, 'voice', key, value.split(u'、'))
            elif key == u'服務處所':
                misc.append_contact(item, 'address', key, value)
            elif key == u'學歷':
                item['education'] = value.split()

        exp_node = tables[1].xpath('.//td[@bgcolor="#FFFFFF"]')
        experience = []
        for ex in exp_node:
            ex = parse.get_inner_text(ex).split()
            experience += ex

        item['experience'] = experience
        m = re.search(u'(副?議長)。?$', item['experience'][0])
        item['title'] = m.group(1) if m else u'議員'
        item['platform'] = parse.get_inner_text(tables[2].xpath('.//td[@bgcolor="#FFFFFF"]')).split()
        return item
