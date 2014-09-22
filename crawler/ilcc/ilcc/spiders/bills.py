# -*- coding: utf-8 -*-
import re
from urlparse import urljoin
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from ilcc.items import Bills
from crawler_lib import parse
from crawler_lib import misc
from scrapy.utils.url import canonicalize_url


class Spider(scrapy.Spider):
    name = "bills"
    base_url = "http://www.hsinchu-cc.gov.tw/Agenda/"
    start_urls = ["http://www.ilcc.gov.tw/Html/H_08/H_08.aspx?change_img=2", ]
    download_delay = 0.5

    def parse(self, response):
        sel = Selector(response)
        viewstate = sel.xpath('//input[@name="__VIEWSTATE"]/@value').extract()[0]

        form_data = dict.fromkeys(
            ['__EVENTTARGET', '__EVENTARGUMENT', '__VIEWSTATE', 'ddlFmotion_category', 'ddlFmotion_property',
             'txtKeyword'], ''
        )
        form_data['btSearch'] = u' -搜尋-'.encode('Big5')
        form_data['__VIEWSTATE'] = viewstate

        return [FormRequest(self.start_urls[0], formdata=form_data, callback=self.parse_index)]


    def parse_index(self, response):
        sel = Selector(response)
        curr_url = response.url

        table = sel.xpath('//table[@id="AutoNumber4"]')
        urls = table.xpath('.//a[contains(@id,"Hyperlink")]/@href').extract()
        for url in urls:
            url = url.encode('Big5')
            url = urljoin(curr_url, url)
            url = canonicalize_url(url)
            yield Request(url, callback=self.parse_bill)

    def parse_bill(self, response):
        response = parse.get_decoded_response(response, 'Big5')
        sel = Selector(response)

        # convert to list of pairs
        rows = sel.xpath('//tr')
        pairs = misc.rows_to_pairs(rows)

        item = Bills()
        item['links'] = response.url
        item['motions'] = []
        main_title = parse.get_inner_text(sel.xpath('//font[@color="#800000"]'), remove_white=True)
        m = re.match(u'宜蘭縣議會(.*)議案資料', main_title)
        if m:
            main_sitting = m.group(1)

        k_map = {
            # u'來源別':'',
            # u'建檔日期':'',
            # u'議案程序':'',
            # u'系統編號':'',
            u'動議人': 'proposed_by',
            u'案號': 'bill_no',
            u'附議人': 'petitioned_by',
            u'類別': 'category',
            # u'小組':'',
            u'案由': 'abstract',
            # u'法規名稱':'',
            u'辦法': 'methods',
            u'理由': 'description',
            # u'附件':'',
            # u'審議日期':'',
            # u'大會決議':'',
        }

        curr_motion = None
        for i, pair in enumerate(pairs):
            n = len(pair)
            if n < 2:
                if n == 1:
                    td = pair[0]
                    text = parse.get_inner_text(td, remove_white=True)
                    if td.xpath(u'.//img[@alt="小圖示"]'):
                        if text != u'案由、辦法、理由及附件':
                            if curr_motion: item['motions'].append(curr_motion)
                            curr_motion = {'motion': text}
                    elif curr_motion is not None and not curr_motion.get('sitting'):
                        curr_motion['sitting'] = ' '.join(td.xpath('.//span/text()').extract())

                continue

            k_raw, v_raw = pair
            k = parse.get_inner_text(k_raw, remove_white=True)
            v = parse.get_inner_text(v_raw)
            k_eng = k_map.get(k)

            if k_eng:
                new_v = v
                if k_eng in ['petitioned_by', 'proposed_by']:
                    new_v = v.split()
                item[k_eng] = new_v
            elif k == u'建檔日期':
                misc.append_motion(item, u'建檔', None, v, main_sitting)

            if curr_motion is not None:
                if u'日期' in k:
                    curr_motion['date'] = v
                elif 'date' in curr_motion:
                    curr_motion['resolution'] = v

        if curr_motion:
            item['motions'].append(curr_motion)

        return item
