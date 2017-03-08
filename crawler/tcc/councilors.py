# -*- coding: utf-8 -*-
import re
import urllib
from urlparse import urljoin
import scrapy


def GetDate(text):
    matchTerm = re.search(u'''
        (?P<year>[\d]+)[\s]*年[\s]*
        (?P<month>[\d]+)[\s]*月[\s]*
        (?P<day>[\d]+)
    ''', text, re.X)
    if matchTerm:
        return '%04d-%02d-%02d' % (int(matchTerm.group('year'))+1911, int(matchTerm.group('month')), int(matchTerm.group('day')))
    else:
        return None

class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.tcc.gov.tw"]
    start_urls = ["http://www.tcc.gov.tw/Councilor_Main.aspx",]
    download_delay = 0.5

    def parse(self, response):
        links = response.xpath('//a[contains(@href, "Councilor_Content.aspx")]/@href').extract()
        for link in links:
            yield scrapy.Request(urljoin(response.url, link), callback=self.parse_profile)

    def parse_profile(self, response):
        item = {}
        image_src = response.xpath('//*[@class="aldermans_photo"]/descendant::img/@src').extract_first()
        item['image'] = urljoin(response.url, urllib.quote(image_src.encode('utf8')))
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        constituency = response.xpath('//div/h3/span[@id="FormView1_ElectionZoneLabel"]/text()').extract_first()
        match = re.search(u'''
            第[\W]{1,3}屆
            (?P<county>[\W]{1,3}(?:縣|市))議員
            [\s]/[\s]
            (?P<selection>第[\W]{1,3}選區)
            [\s]
            （(?P<district>[\S]*)）
        ''', constituency, re.X)
        if match:
            item['constituency'] = '%s%s' % (match.group('county'), match.group('selection'))
            item['county'] = match.group('county')
            item['district'] = match.group('district')
        nodes = response.xpath('//table[@class="aldermans_information"]/tr')
        item['name'] = re.sub(u'\s|　', '', response.xpath(u'string(//td[re:test(., "姓\s*名")]/following-sibling::td[1])').extract_first())
        item['gender'] = re.sub(u'\s|　', '', response.xpath(u'string(//td[re:test(., "性\s*別")]/following-sibling::td[1])').extract_first())
        item['birth'] = GetDate(re.sub(u'\s|　', '', response.xpath(u'string(//td[re:test(., "出\s*生")]/following-sibling::td[1])').extract_first()))
        item['party'] = re.sub(u'\s|　', '', response.xpath(u'string(//td[re:test(., "黨\s*籍")]/following-sibling::td[1])').extract_first())
        link = re.sub(u'\s|　', '', response.xpath(u'string(//td[re:test(., "個人網站")]/following-sibling::td[1])').extract_first())
        item['links'].append({'url': link, 'note': u'個人網站'})
        item['contact_details'] = []
        contact_mappings = {
            u'電話': 'voice',
            u'傳真': 'fax',
            u'通訊處': 'address',
            u'電子信箱': 'email'
        }
        for label, name in contact_mappings.items():
            values = [x.strip() for x in response.xpath(u'//td[re:test(., "%s")]/following-sibling::td[1]/descendant::*/text()' % '\s*'.join(label)).extract() if x.strip()]
            for value in values:
                item['contact_details'].append({
                    'label': label,
                    'type': name,
                    'value': value
                })
        item['education'] = [x.strip() for x in response.xpath(u'//td[re:test(., "學\s*歷")]/following-sibling::td[1]/descendant::*/text()').extract() if x.strip()]
        item['experience'] = [x.strip() for x in response.xpath(u'//td[re:test(., "經\s*歷")]/following-sibling::td[1]/descendant::*/text()').extract() if x.strip()]
        item['platform'] = [x.strip() for x in response.xpath(u'//*[re:test(., "政\s*見")]/ancestor::tr/following-sibling::tr[1]/descendant::*/text()').extract() if x.strip()]
        remark = response.xpath(u'normalize-space(string(//*[re:test(., "備\s*註")]/ancestor::tr/following-sibling::tr[1]/descendant::*/text()))').extract_first()
        item['remark'] = remark.strip() if remark.strip() else ''
        item['election_year'] = '2014'
        item['in_office'] = True
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': '2018-12-24'}
        yield item
