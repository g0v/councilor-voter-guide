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
        nodes = sel.xpath(u'//td/table/tbody/tr/td/a/img[contains(@title, "原住民")]')
        for node in nodes:
            district = node.xpath('@title').re(u'：(.+)')[0]
            yield Request(self.base_url + node.xpath('../@href').extract()[0].strip(), callback=self.parse_profile, meta={'district': district})
        nodes = sel.xpath('//td/table/tbody/tr/td//a[contains(@href, "u_editor_v1.asp")]')
        for node in nodes:
            if node.xpath('img'):
                continue
            try:
                district = node.xpath('..//text()').re(u'\((.+)\)')
                if district:
                   district = district[0].strip()
                else:
                   district = node.xpath('../..//text()').re(u'\((.+)\)')[0].strip()
                href = node.xpath('@href').extract()[0].strip()
                url = href if self.base_url in href else self.base_url + href
                yield Request(url, callback=self.parse_profile, meta={'district': district})
            except Exception, e:
                print e
                print node.xpath('..//text()').re(u'\((.+)\)')
                print node.xpath('..//text()').extract()
                print node.xpath('@href').extract()[0]

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
        item['county'] = u'臺中市'
        item['district'] = response.request.meta['district']
        item['image'] = get_extracted(sel.xpath(u'//img[contains(@alt, "照片")]/@src'))
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        item['in_office'] = True
        item['contact_details'] = []
        main_node = sel.xpath('//td[@class="C-tableA3"]/div')
        basic_info_node = main_node.xpath('table[1]/tbody/tr/td/table/tbody')
        for tr in basic_info_node.xpath('tr'):
            th = get_extracted(tr.xpath('th/*/text()')).strip()
            td = get_extracted(tr.xpath('td[1]/text()')).strip()
            if th == u'姓名':
                text = td.split()
                item['name'] = text[0].rstrip(u'議員')
                item['title'] = text[1] if len(text) > 1 else u'議員'
            elif th == u'政黨':
                item['party'] = td
            elif th == u'屆別':
                match = re.search(u'.*第(?P<Nth>.*)屆', td, re.X)
                if match:
                    Nth = match.group('Nth')
                    item['election_year'] = self.election_year_dict.get(Nth)
            elif th == u'選區':
                item['constituency'] = td
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
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': '%d-12-25' % (int(item['election_year']) + 4)}
        return item
