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
import logging


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

        # XXX hack for correcting information

        special_url = "http://www.tycc.gov.tw/page.aspx?wtp=1&wnd=204&town=%E5%B1%B1%E5%9C%B0%E5%8E%9F%E4%BD%8F%E6%B0%91"
        yield Request(special_url, callback=self.parse_selection_index)

    def parse_selection_index(self, response):
        sel = Selector(response)
        urls = sel.xpath('//div[@id="ctl04_ctl08_pageControl_PN_LIST"]//a/@href').extract()
        for url in urls:
            url = urljoin(response.url, url)
            logging.info('to request id: url: %s', url)
            yield Request(url, callback=self.parse_profile)

    def parse_profile(self, response):
        sel = Selector(response)

        main_node = sel.xpath('//table[@class="specpage_data_table"]//table[2]')
        info_node = main_node.xpath('.//table[2]')
        curr_url = response.url

        logging.info('to setup item: curr_url: %s', curr_url)

        item = Councilor()
        item['contact_details'] = []
        item['name'] = \
            info_node.xpath('.//span[@id="ctl04_ctl08_pageControl_LB_MEM_NAME"]/text()').extract()[0].split()[0]
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        img_url = main_node.xpath('.//img[@class="memImg"]/@src').extract()[0]
        item['image'] = urljoin(curr_url, img_url)

        logging.info('after image: item: %s', item)

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
                logging.info('info: %s', info)

                address_str = info[0]
                if u'電話:' not in info[1]:
                    address_str += info[1]
                address = re.sub(ur'.*服務處.*：', '', address_str).strip()
                misc.append_contact(item, 'address', '服務處', address)

                for group in info:
                    if re.search(ur'電話:', group):
                        tel_val = re.sub(ur'/.*', '', re.sub(ur'.*電話:', '', group)).strip()
                        if tel_val:
                            misc.append_contact(item, 'voice', '電話', tel_val)
                    if re.search(ur'傳真:', group):
                        fax_val = re.sub(ur'/.*', '', re.sub(ur'.*傳真:', '', group)).strip()
                        if fax_val:
                            misc.append_contact(item, 'fax', '傳真', fax_val)

            td = row.xpath('./td[2]')
            value = parse.get_inner_text(td)
            if not value:
                continue

            logging.info('contact_info: key: %s value: %s td: %s is_contact_info: %s', key, value, td, is_contact_info)

            k_eng = key_map.get(key)
            if is_contact_info:
                blog_url = td.xpath('.//span[@id="ctl04_ctl08_pageControl_LB_MEM_BLOG"]/a/@href').extract()
                if blog_url:
                    blog_url = blog_url[0].strip()
                    logging.info('blog_url: %s dir: %s', blog_url, dir(blog_url))
                    item['links'].append({"url": blog_url, "note": "部落格"})

                facebook_url = td.xpath('.//span[@id="ctl04_ctl08_pageControl_LB_MEM_FACEBOOK"]/a/@href').extract()
                if facebook_url:
                    facebook_url = facebook_url[0].strip()
                    logging.info('facebook_url: %s', facebook_url)
                    item['links'].append({"url": facebook_url, "note": "臉書"})

                emails = td.xpath('.//span[@id="ctl04_ctl08_pageControl_LB_MEM_EMAIL"]/a/@href').extract()
                if emails:
                    emails = emails[0]
                    emails = emails.split(';')
                    emails = [re.sub(ur'^mailto://', '', email.strip()) for email in emails]
                    logging.info('emails: %s', emails)
                    for each_email in emails:
                        misc.append_contact(item, 'email', 'EMAIL', each_email)
            elif k_eng:
                values = parse.get_inner_text_lines(td)
                values = [parse.remove_whitespaces(v) for v in values]
                item[k_eng] = values
            elif key == u'選區':
                split = value.split()
                item['county'] = county
                item['district'] = split[1] if len(split) > 1 else ''
                item['constituency'] = county + split[0]

        # XXX hack for correcting information
        if item['name'] == u'張火爐':
            item['district'] = u'楊梅市'
        if item['name'] == u'李家興':
            item['district'] = u'楊梅市'

        logging.info('to return: item: %s', item)

        return item
