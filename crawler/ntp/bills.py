# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from ..items import Bills


def ROC2AD(text):
    matchTerm = re.search(u'''
        (?P<year>[\d]+)[\s]*(?:年|[-/.])[\s]*
        (?P<month>[\d]+)[\s]*(?:月|[-/.])[\s]*
        (?P<day>[\d]+)
    ''', text, re.X)
    if matchTerm:
        return '%04d-%02d-%02d' % (int(matchTerm.group('year'))+1911, int(matchTerm.group('month')), int(matchTerm.group('day')))
    else:
        return None

class Spider(scrapy.Spider):
    name = "bills"
    allowed_domains = ["bms.ntp.gov.tw"]
    start_urls = ['http://bms.ntp.gov.tw/NewTCAV/BillQuery/BillQuery_Form_Context.aspx?BillNO=%d' % i for i in range(5000, 9000)]
    election_year = {'1': '2010', '2': '2014'}
    #download_delay = 0.5

    def parse(self, response):
        item = Bills()
        sel = Selector(response)
        try:
            item['election_year'] = self.election_year[sel.xpath('//span[@id="lab_MDSL"]/text()').re(u'第(\d+)屆')[0]]
        except:
            return
        item['county'] = u'新北市'
        item['id'] = re.findall(u'=(\d+)$', response.url)[0]
        item['type'] = sel.xpath('//span[@id="lab_BillType"]/text()').extract()[0].strip() if sel.xpath('//span[@id="lab_BillType"]/text()').extract() else ''
        item['category'] = sel.xpath('//span[@id="lab_BillClass"]/text()').extract()[0].strip() if sel.xpath('//span[@id="lab_BillClass"]/text()').extract() else ''
        item['proposed_by'] = sel.xpath('//span[@id="lab_Provider"]/text()').extract()[0].strip().split(u',') if sel.xpath('//span[@id="lab_Provider"]/text()').extract() else []
        item['petitioned_by'] = sel.xpath('//span[@id="lab_SupportMan"]/text()').extract()[0].strip().split(u',') if sel.xpath('//span[@id="lab_SupportMan"]/text()').extract() else []
        item['abstract'] = '\n'.join([re.sub('\s', '', x) for x in sel.xpath('//span[@id="lab_Reason"]/div//text()').extract()])
        item['description'] = '\n'.join([re.sub('\s', '', x) for x in sel.xpath('//span[@id="lab_Description"]/div//text()').extract()])
        item['methods'] = '\n'.join([re.sub('\s', '', x) for x in sel.xpath('//span[@id="lab_Method"]/div/text()').extract()])
        motions = []
        motions.append(dict(zip(['motion', 'resolution', 'date'], [u'一讀決議', '\n'.join([re.sub('\s', '', x) for x in sel.xpath('//span[@id="lab_OneResult"]//text()').extract()]), None])))
        motions.append(dict(zip(['motion', 'resolution', 'date'], [u'審查意見', '\n'.join([re.sub('\s', '', x) for x in sel.xpath('//span[@id="lab_ExamResult"]//text()').extract()]), None])))
        motions.append(dict(zip(['motion', 'resolution', 'date'], [u'大會決議', '\n'.join([re.sub('\s', '', x) for x in sel.xpath('//span[@id="lab_Result"]//text()').extract()]), None])))
        motions.append(dict(zip(['motion', 'resolution', 'date'], [u'二讀決議', '\n'.join([re.sub('\s', '', x) for x in sel.xpath('//span[@id="lab_TwoResult"]//text()').extract()]), None])))
        motions.append(dict(zip(['motion', 'resolution', 'date'], [u'三讀決議', '\n'.join([re.sub('\s', '', x) for x in sel.xpath('//span[@id="lab_ThreeResult"]//text()').extract()]), None])))
        item['motions'] = motions
        item['links'] = response.url
        return item
