# -*- coding: utf-8 -*-
import re
import urllib
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from hccc.items import Bills
from crawler_lib import parse
from crawler_lib import misc


class Spider(scrapy.Spider):
    name = "bills"
    base_url = "http://www.hsinchu-cc.gov.tw/Agenda/"
    start_urls = ["http://www.hsinchu-cc.gov.tw/Agenda/Agenda.htm", ]
    download_delay = 0.5

    def parse(self, response):
        sel = Selector(response)
        rows = sel.xpath('//table[@bordercolordark="#4292d6"]/tbody/tr')
        sitting = None
        for row in rows:
            text = ''.join(row.xpath('.//text()').extract()).strip()
            text = parse.remove_whitespaces(text)
            if not text:
                continue

            if re.match(u'第.*屆', text):
                sitting = text
                continue

            anchors = row.xpath(".//a")
            links = []
            for anchor in anchors:
                link_text = parse.get_inner_text(anchor)
                if link_text:
                    links.append(anchor.xpath('@href').extract()[0])

            url = parse.take_first(links)
            item = Bills()
            print sitting, text

            if url:
                url = self.base_url + url
                yield Request(url, callback=self.parse_files, meta={
                    'item': item
                })

    def parse_files(self, response):
        sel = Selector(response)
        meta = response.request.meta
        item = meta['item']
        rows = sel.xpath('//table[@bordercolordark="#4292d6"]/tbody/tr')
        for row in rows:
            anchors = row.xpath('.//a')
            if anchors:
                text = parse.get_inner_text(row)
                url = anchors.xpath('@href').extract()
                url = parse.take_first(url)
                print text, url
        return item
