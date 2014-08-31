# -*- coding: utf-8 -*-
import re
import urllib
from urlparse import urljoin
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from tccc.items import Councilor


def take_first(list_in):
    if len(list_in) == 1:
        return list_in[0]
    else:
        return ''


def get_extracted(xpath):
    return take_first(xpath.extract())


def GetDate(text):
    matchTerm = re.search(u'''
        (?P<year>[\d]+)[\s]*年[\s]*
        (?P<month>[\d]+)[\s]*月[\s]*
        (?P<day>[\d]+)
    ''', text, re.X)
    if matchTerm:
        return '%04d-%02d-%02d' % (
            int(matchTerm.group('year')) + 1911, int(matchTerm.group('month')), int(matchTerm.group('day')))
    else:
        return None


class Spider(scrapy.Spider):
    name = "councilors"
    base_url = "http://www.tccc.gov.tw"
    allowed_domains = ["www.tccc.gov.tw"]
    start_urls = ["http://www.tccc.gov.tw/editor_model/u_editor_v1.asp?id={762491FF-702E-4D53-9B35-12FF20DA7AE1}", ]
    download_delay = 0.5
    election_year_dict = {
        u'一': '2010'
    }

    def parse(self, response):
        sel = Selector(response)
        nodes = sel.xpath('//td/table/tbody/tr/td//a[contains(@href, "u_editor_v1.asp")]')
        for node in nodes:
            text = get_extracted(node.xpath('text()')).strip()
            if text:
                href = get_extracted(node.xpath('@href'))
                url = href if self.base_url in href else self.base_url + href
                # print url
                yield Request(url, callback=self.parse_profile)

    def append_contact(self, item, contact_type, label, value):
        item['contact_details'].append({'type': contact_type, 'label': label, 'value': value})

    def append_contact_list(self, item, contact_type, label, value_list):
        for value in value_list:
            item['contact_details'].append({'type': contact_type, 'label': label, 'value': value})

    def extract_and_strip(self, xpath):
        items = xpath.extract()
        return filter(None, [item.strip() for item in items])

    def parse_profile(self, response):
        # print '#' * 50
        sel = Selector(response)
        item = Councilor()
        item['contact_details'] = []

        image = get_extracted(sel.xpath(u'//img[contains(@alt, "照片")]/@src'))
        main_node = sel.xpath('//td[@class="C-tableA3"]/div')
        basic_info_node = main_node.xpath('table[1]/tbody/tr/td/table/tbody')

        # print  basic_info_node
        for tr in basic_info_node.xpath('tr'):
            th = get_extracted(tr.xpath('th/*/text()')).strip()
            td = get_extracted(tr.xpath('td[1]/text()')).strip()
            # print td, type(td) ,th
            # if
            # td = td.decode('utf-8')

            if th == u'姓名':
                for title in [u'副議長', u'議長', u'議員']:
                    td = td.rstrip(title).strip()
                item['name'] = td
            elif th == u'政黨':
                item['party'] = td
            elif th == u'屆別':
                match = re.search(u'.*第(?P<Nth>.*)屆', td, re.X)
                if match:
                    Nth = match.group('Nth')
                    item['election_year'] = self.election_year_dict.get(Nth)
            elif th == u'選區':
                match = re.search(u'第(?P<number>[0-9]*)選區', td, re.X)
                chinese_number = [
                    "", u"一", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九", u"十",
                    u"十一", u"十二", u"十三", u"十四", u"十五", u"十六", u"十七", u"十八", u"十九",
                ]
                if match:
                    number = int(match.group('number'))
                    if number < len(chinese_number):
                        item['constituency'] = u'臺中市第%s選區' % chinese_number[number]
            elif th == u'服務處地址':
                self.append_contact(item, 'address', u'服務處地址', td)
            elif th == u'服務處電話':
                phones = [phone.strip() for phone in td.split('/')]
                self.append_contact_list(item, 'voice', u'服務處電話', phones)
            elif th == u'服務處傳真':
                faxes = [fax.strip() for fax in td.split('/')]
                self.append_contact_list(item, 'fax', u'服務處傳真', faxes)
            elif th == u'e-mail':
                emails = tr.xpath('td/a/text()').extract()
                self.append_contact_list(item, 'email', u'e-mail', emails)

        item['education'] = self.extract_and_strip(main_node.xpath('table[2]/tbody/tr[3]/td/ul/li/text()'))
        item['experience'] = self.extract_and_strip(main_node.xpath('table[3]/tbody/tr[3]/td/ul/li/text()'))
        item['platform'] = self.extract_and_strip(main_node.xpath('table[4]/tbody/tr[3]/td/ol/li/text()'))

        return item
