# -*- coding: utf-8 -*-
from collections import defaultdict
import os
import re
import time
import subprocess
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from tccc.items import MeetingMinutes


def take_first(list_in):
    if len(list_in) == 1:
        return list_in[0]
    else:
        raise


class Spider(scrapy.Spider):
    name = "meeting"
    allowed_domains = ["www.tccc.gov.tw"]
    base_url = 'http://www.tccc.gov.tw'
    knowledge_url = 'http://www.tccc.gov.tw/govknowledge/'
    start_urls = ["http://www.tccc.gov.tw/editor_model/u_editor_v1.asp?id={24BDFA69-2A9C-49ED-A795-83327F8894D9}", ]
    download_delay = 0.5

    def parse(self, response):
        sel = Selector(response)
        nodes = sel.xpath('//*[@id="content"]//table//a[@class="table-way-link"]')

        for node in nodes:
            href = node.xpath('@href').extract()[0]
            text = ''.join(node.xpath('*//text()').extract()).strip()
            url = self.base_url + href
            callback = lambda res: self.parse_ordinal(res, text)
            yield Request(url, callback=callback)

    # 第n屆頁面
    def parse_ordinal(self, response, ordinal):
        sel = Selector(response)
        links = sel.xpath('//table[@class="C-tableA0"]//a')
        for link in links:
            text = link.xpath('text()').extract()[0]
            if text == u'議事錄':
                href = link.xpath('@href').extract()[0]
                url = self.knowledge_url + href
                callback = lambda res: self.parse_meeting_list(res, ordinal)
                yield Request(url, callback=callback)

    def parse_meeting_list(self, response, ordinal):
        sel = Selector(response)
        links = sel.xpath('//table[@class="C-tableA0"]//a')

        meeting_map = {}
        read_record_map = defaultdict(dict)
        for link in links:
            text = link.xpath('text()').extract()[0].strip()
            href = link.xpath('@href').extract()[0]
            url = self.knowledge_url + href
            if not href:
                continue

            m = re.search(u'(第[0-9]+次.*會)\((.*)\)-?([0-9]*)', text)
            meeting = None
            date_range = None
            page = None
            if m:
                meeting, date_range, page = m.groups()

            meeting = meeting or text

            item = meeting_map.get(meeting) or MeetingMinutes()
            item['sitting'] = ordinal
            item['meeting'] = meeting
            item['download_url'] = []

            if date_range:
                item['date'] = date_range

            meeting_map[meeting] = item
            if page:
                read_record_map[meeting][page] = False

            callback = lambda res: self.parse_file_list(res, ordinal)
            yield Request(url, callback=callback, meta={
                'item': item,
                'read_record': read_record_map[meeting] if page else None,
                'page': page
            })

    def parse_file_list(self, response, ordinal):
        sel = Selector(response)
        meta = response.request.meta
        item = meta['item']
        rows = sel.xpath('//table[@class="C-tableA0"]//tr/td[2]')
        file_list = []
        for row in rows:
            links = row.xpath('.//a')
            if not links:
                continue

            link = links[0]
            text = row.xpath('text()').extract()[0].strip()
            href = link.xpath('@href').extract()[0]
            url = self.base_url + href
            file_list.append({
                'url': url,
                'text': text
            })
            if os.path.exists('../../meeting_minutes/tccc/2010_%s.pdf' % text):
                continue
            cmd = 'wget -c -O ../../meeting_minutes/tccc/2010_%s.pdf %s' % (text, url)
            retcode = subprocess.call(cmd, shell=True)
            time.sleep(1)

        item['download_url'].extend(file_list)

        read_record = meta['read_record']
        if read_record:
            read_record[meta['page']] = True  # set as read

        # return item only when all file lists are read
        if not read_record or all(read_record.values()):
            return item

