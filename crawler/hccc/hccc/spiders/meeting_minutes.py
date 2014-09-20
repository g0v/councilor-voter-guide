# -*- coding: utf-8 -*-
import os
import time
import scrapy
from scrapy.http import Request, FormRequest, HtmlResponse
from scrapy.selector import Selector
from hccc.items import MeetingMinutes
from crawler_lib import parse
from crawler_lib import misc


class Spider(scrapy.Spider):
    name = "meeting"
    start_urls = ["http://www.hsinchu-cc.gov.tw/search/Issue.asp", ]
    download_delay = 0.5

    def start_requests(self):
        payload = {
            'ord1': '',
            'ord': '',
            'seq': '',
            'Cname': '',
            'B1': ''
        }
        return [FormRequest(self.start_urls[0], formdata=payload, callback=self.parse)]

    def parse(self, response):
        response = parse.get_decoded_response(response, 'Big5')
        sel = Selector(response)

        table = sel.xpath('//table[@bordercolordark="#4ab69c"]')
        for i, tr in enumerate(table.xpath('tr')):
            if i == 0:
                continue

            item = MeetingMinutes()
            cols = [td.xpath('.//text()').extract()[0].strip() for td in tr.xpath('td')]
            item['sitting'] = cols[0]
            item['date'] = cols[1]
            item['councilor'] = cols[2]
            # item['meeting'] = meeting
            download_urls = tr.xpath('.//a/@href').extract()
            item['download_url'] = download_urls

            for url in download_urls:
                filename = os.path.basename(url)
                if not filename:
                    continue

                file_path = '../../meeting_minutes/hccc/' + filename
                result = misc.download(url, file_path)
                if not result['skipped']:
                    time.sleep(1)

            yield item
