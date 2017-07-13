# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
import urllib
import scrapy

import common


class Spider(scrapy.Spider):
    name = "bills"
    allowed_domains = ["www.tcc.gov.tw", "tccmis.tcc.gov.tw"]
    start_urls = ["http://www.tcc.gov.tw"]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    ads = {'1969': 1, '1973': 2, '1977': 3, '1981': 4, '1985': 5, '1989': 6, '1994': 7, '1998': 8, '2002': 9, '2006': 10, '2010': 11, '2014': 12, '2018': 13}
    ad = ads[election_year]

    def parse(self, response):
        return response.follow(response.xpath(u'//a[re:test(., "^議事資訊系統$")]/@href').extract_first(), callback=self.parse_frame)

    def parse_frame(self, response):
        return response.follow(response.xpath('//frame[@name="Search"]/@src').extract_first(), callback=self.parse_form)

    def parse_form(self, response):
        return scrapy.FormRequest.from_response(response, formname='OMForm', formdata={'OmasDetr': str(self.ad), 'rdoDE': '0'}, callback=self.parse_post)

    def parse_post(self, response):
        for node in response.xpath('//tr[@id="tr"]'):
            item = {}
            td = node.xpath('td/text()').extract()
            item['election_year'] = self.election_year
            item['id'] = td[1]
            item['bill_no'] = td[2]
            item['type'] = re.sub('\s', '', td[3])
            item['category'] = td[4]
            yield scrapy.Request("http://tccmis.tcc.gov.tw/OM/OM_SearchDetail.asp?sys_no=%s" % item['id'], callback=self.parse_profile, meta={'item': item})

    def parse_profile(self, response):
        item = response.meta['item']
        nodes = response.xpath('//div[@id="detail"]/table/tr')
        motions, committee_motion, council_motion = [], {}, {}
        for node in nodes:
            if node.xpath('td/text()')[0].re(u'目前處理程序'):
                item['last_action'] = node.xpath('td/text()').extract()[1]
            elif node.xpath('td/text()')[0].re(u'案由'):
                item['abstract'] = node.xpath('td/text()').extract()[1]
            elif node.xpath('td/text()')[0].re(u'提案人'):
                item['proposed_by'] = node.xpath('td/div/text()').extract()[0].strip().split(u'、')
            elif node.xpath('td/text()')[0].re(u'召集人/委員'):
                item['proposed_by'] = node.xpath('td/text()').extract()[1].strip().split(u'、')
            elif node.xpath('td/text()')[0].re(u'議決會次'):
                council_motion['motion'] = u'大會議決'
                council_motion['date'] = common.ROC2AD(node.xpath('td/text()').extract()[1].split()[0])
                council_motion['sitting'] = ''.join(node.xpath('td/text()').extract()[1].split()[1:])
            elif node.xpath('td/text()')[0].re(u'議決文'):
                council_motion['resolution'] = node.xpath('td/text()').extract()[1]
            elif node.xpath('td/text()')[0].re(u'案(\s|　)+?號'):
                item['bill_no'] = node.xpath('td/text()').extract()[1].strip()
            elif node.xpath('td/text()')[0].re(u'來文文號'):
                td = node.xpath('td/text()').extract()[1].split()
                d = dict(zip(['motion', 'resolution', 'date'], [u'來文', None, common.ROC2AD(td[0])]))
                if len(td) > 1:
                    d['no'] = td[1]
                motions.append(d)
            elif node.xpath('td/text()')[0].re(u'收文日期'):
                motions.append(dict(zip(['motion', 'resolution', 'date'], [u'收文', None, common.ROC2AD(node.xpath('td/text()').extract()[1])])))
            elif node.xpath('td/text()')[0].re(u'審查日期'):
                committee_motion['motion'] = u'委員會審查意見'
                committee_motion['date'] = common.ROC2AD(node.xpath('td/text()').extract()[1])
            elif node.xpath('td/text()')[0].re(u'審查意見'):
                committee_motion['resolution'] = '\n'.join(node.xpath('td/text()').extract()[1:])
            elif node.xpath('td/text()')[0].re(u'發文文號'):
                td = node.xpath('td/text()').extract()[1].split()
                d = dict(zip(['motion', 'resolution', 'date'], [u'發文', None, common.ROC2AD(td[0])]))
                if len(td) > 1:
                    d['no'] = td[1]
                motions.append(d)
            elif node.xpath('td/text()')[0].re(u'執行情形'):
                item['execution'] = node.xpath('td/text()').extract()[1]
            elif node.xpath('td/text()')[0].re(u'備[\s]*?註'):
                item['remark'] = '\n'.join(node.xpath('td/text()').extract()[1:])
        for motion in [committee_motion, council_motion]:
            if motion:
                motions.append(motion)
        item['motions'] = sorted(motions, key=lambda x: x.get('date'), reverse=True)
        item['links'] = response.url
        return item
