# -*- coding: utf-8 -*-
import re
import scrapy
from urlparse import urljoin


def GetDate(text):
    matchTerm = re.search(u'''
        (?P<year>[\d]+)[\s]*(年|[.])[\s]*
        (?P<month>[\d]+)[\s]*(月|[.])[\s]*
        (?P<day>[\d]+)
    ''', text, re.X)
    if matchTerm:
        return '%04d-%02d-%02d' % (int(matchTerm.group('year'))+1911, int(matchTerm.group('month')), int(matchTerm.group('day')))
    else:
        return None

class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.kcc.gov.tw"]
    start_urls = ["http://www.kcc.gov.tw/PeriodMembers/MainMap.aspx",]
    download_delay = 0.5

    def parse(self, response):
        nodes = response.xpath('//map[@id="imgsmapMap"]/area')
        for node in nodes:
            constituency = node.xpath('@title').re(u'連結至(第\d+選區)')[0]
            area_id = node.xpath('@href').re(u'#(.+)')[0]
            area_node = response.xpath('//a[@id="%s"]' % area_id)[0]
            district = u'、'.join(area_node.xpath('following::ul').css('.all_area')[0].xpath('li/text()').extract())
            for person in area_node.xpath('following::ul').css('.embers_mame')[0].xpath('li/a'):
                item = {}
                item['name'] = re.sub(u'\(已.*\)', '', person.xpath('text()').extract_first())
                item['constituency'] = constituency
                item['district'] = district
                yield scrapy.Request(urljoin(response.url, person.xpath('@href').extract_first()), callback=self.parse_profile, meta={'item': item})

    def parse_profile(self, response):
        item = response.meta['item']
        item['county'] = u'高雄市'
        item['election_year'] = '2014'
        item['in_office'] = True
        item['term_start'] = '%s-12-25' % item['election_year']
        item['term_end'] = {'date': '2018-12-24'}
        image_src = response.xpath('//img[@id="ContentPlaceHolder1_lv_Pic_0"]/@src').extract_first()
        item['image'] = urljoin(response.url, image_src)
        item['links'] = [{'url': response.url, 'note': u'議會個人官網'}]
        for link in response.xpath(u'//th[re:test(., "網站連結：")]')[-1].xpath('following-sibling::td[1]/a'):
            item['links'].append({
                'url': link.xpath('@href').extract_first(),
                'note': link.xpath('text()').extract_first().strip()
            })
        item['title'] = response.css('.form_bk-line').xpath('h4/text()').re(u'(議長|副議長|議員)')[0]
        item['gender'] = response.xpath(u'//th[re:test(., "性[\s　]*別：")]')[-1].xpath('following-sibling::td[1]/text()').extract_first().strip()
        item['party'] = response.xpath(u'//th[re:test(., "所屬政黨：")]')[-1].xpath('following-sibling::td[1]/descendant::td[1]/text()').extract_first().strip()
        item['contact_details'] = []
        contact_mappings = {
            u'聯絡電話': 'voice',
            u'傳真電話': 'fax',
            u'通訊地址': 'address',
            u'電子郵件': 'email',
        }
        for label, name in contact_mappings.items():
            values = [x.strip() for x in response.xpath(u'//th[re:test(., "%s：")]' % '\s*'.join(label))[-1].xpath('string(following-sibling::td[1])').extract() if x.strip()]
            for value in values:
                item['contact_details'].append({
                    'label': label,
                    'type': name,
                    'value': value
                })
        item['education'] = [x.strip() for x in response.xpath(u'//th[re:test(., "學[\s　]*歷：")]')[-1].xpath('following-sibling::td[1]/*/text()').extract() if x.strip()]
        item['experience'] = [x.strip() for x in response.xpath(u'//th[re:test(., "經[\s　]*歷：")]')[-1].xpath('following-sibling::td[1]/*/text()').extract() if x.strip()]
        item['platform'] = [x.strip() for x in response.xpath(u'//th[re:test(., "服務政見：")]')[-1].xpath('following-sibling::td[1]/*/text()').extract() if x.strip()]
        remark = response.xpath(u'//th[re:test(., "備[\s　]*註：")]')
        if remark:
            item['remark'] = remark[-1].xpath('following-sibling::td[1]/descendant::*/text()').extract_first().strip()
            m = re.search(u'已', item['remark'])
            if m:
                item['in_office'] = False
                item['term_end'] = {
                    'date': GetDate(item['remark']),
                    'reason': item['remark']
                }
        yield item
