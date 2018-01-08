# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
from urlparse import urljoin
import scrapy

import common


class Spider(scrapy.Spider):
    name = "bills"
    allowed_domains = ["ntp.gov.tw"]
    start_urls = ['http://www.ntp.gov.tw/index.aspx?FType=mb']
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    ads = {'2010': 1, '2014': 2, '2018': 3}
    ad = ads[election_year]

    def parse(self, response):
        return response.follow(response.xpath(u'//img[@alt="議事資訊"]/parent::a/@href').extract_first(), callback=self.parse_tab)

    def parse_tab(self, response):
        return response.follow(response.xpath(u'//a[re:test(., "議案查詢")]/@href').extract_first(), callback=self.parse_frame)

    def parse_frame(self, response):
        return response.follow(response.xpath(u'//iframe[@title="議案查詢介面"]/@src').extract_first(), callback=self.parse_query)

    def parse_query(self, response):
        payload = {'dd_MJ': response.xpath(u'//select[@name="dd_MJ"]/option[re:test(., "%s")]/@value' % self.ad).extract_first()}
        return scrapy.FormRequest.from_response(response, formname='Form1', formdata=payload, callback=self.parse_list)

    def parse_list(self, response):
        for node in response.xpath('//table[@id="dg_List"]/tr[position()>1 and position()<last()]'):
            yield response.follow(node.xpath('td[1]/input/@onclick').re(u"open\('(.*?=\d+)")[0], callback=self.parse_profile)
        if response.css('.MultiPageButtonFont span::text').re('1$'):
            payload = {name: None for name in response.xpath('////input[not(@type="hidden")]/@name').extract()}
            for page in response.css('.MultiPageButtonFont').xpath('descendant::span[1]/following-sibling::a'):
                payload['__EVENTTARGET'] = page.xpath('@href').re("doPostBack\('([^']*)'")[0]
                yield scrapy.FormRequest.from_response(response, formdata=payload, callback=self.parse_list, dont_filter=True, dont_click=True, headers=common.headers(self.county_abbr))

    def parse_profile(self, response):
        item = {}
        item['election_year'] = self.election_year
        item['id'] = re.search(u'BillNO=(\d+)', response.url).group(1).zfill(6)
        item['type'] = response.xpath('//span[@id="lab_BillType"]/text()').extract_first().strip() if response.xpath('//span[@id="lab_BillType"]/text()').extract() else ''
        item['category'] = response.xpath('//span[@id="lab_BillClass"]/text()').extract_first().strip() if response.xpath('//span[@id="lab_BillClass"]/text()').extract() else ''
        item['proposed_by'] = response.xpath('//span[@id="lab_Provider"]/text()').extract_first().strip().split(u',') if response.xpath('//span[@id="lab_Provider"]/text()').extract() else []
        item['petitioned_by'] = (response.xpath('//span[@id="lab_SupportMan"]/text()').extract_first() or '').strip().split(u',')
        item['abstract'] = '\n'.join([re.sub('\s', '', x) for x in response.xpath('//span[@id="lab_Reason"]/div//text()').extract()])
        item['description'] = '\n'.join([re.sub('\s', '', x) for x in response.xpath('//span[@id="lab_Description"]/div//text()').extract()])
        item['methods'] = '\n'.join([re.sub('\s', '', x) for x in response.xpath('//span[@id="lab_Method"]/div/text()').extract()])
        motions = []
        for motion, id in [(u'市府回覆', 'dg_Response__ctl2_lab_dgReplyDesc'), (u'一讀決議', 'lab_OneResult'), (u'審查意見', 'lab_ExamResult'), (u'大會決議', 'lab_Result'), (u'二讀決議', 'lab_TwoResult'), (u'三讀決議', 'lab_ThreeResult'), ]:
            content = '\n'.join([re.sub('\s', '', x) for x in response.xpath('//span[@id="%s"]//text()' % id).extract()])
            if content:
                motions.append(dict(zip(['motion', 'resolution', 'date'], [motion, content, None])))
        item['motions'] = motions
        item['links'] = [
            {
                'url': response.url,
                'note': 'original'
            }
        ]
        return item
