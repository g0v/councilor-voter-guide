# -*- coding: utf-8 -*-
import re
import urllib
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from tcc.items import Bills


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
    name = "bills"
    allowed_domains = ["tccmis.tcc.gov.tw"]
    start_urls = ["http://tccmis.tcc.gov.tw/OM/OM_SearchList.asp",]
    download_delay = 0.5

    def start_requests(self):
        payload = {
            'FTSearch': u'ON',
            'pagesize': u'20',
            'omastext': u'',
            'rdoDE': u'0',
            'OmasDetr': u'11',
            'OmasDetp': u'',
            'OmasDetm': u'',
            'sDateY': u'',
            'sDateM': u'',
            'sDateD': u'',
            'eDateY': u'',
            'eDateM': u'',
            'eDateD': u'',
            'spek': u''
        }
        return [FormRequest("http://tccmis.tcc.gov.tw/OM/OM_SearchList.asp", formdata=payload, callback=self.parse)]

    def parse(self, response):
        sel = Selector(response)
        items = []
        nodes = sel.xpath('//div/table/tr[@id="tr"]')
        for node in nodes:
            item = Bills()
            td = node.xpath('td/text()').extract()
            item['id'] = td[1].encode('latin1').decode('big5')
            item['type'] = ''.join(td[2].encode('latin1').decode('big5').split())
            item['category'] = td[3].encode('latin1').decode('big5')
            request = Request("http://tccmis.tcc.gov.tw/OM/OM_SearchDetail.asp?sys_no=%s" % item['id'], callback=self.parse_profile)
            request.meta['item'] = item
            yield request

    def parse_profile(self, response):
        sel = Selector(response)
        item = response.request.meta['item']
        nodes = sel.xpath('//div[@id="detail"]/table/tr')

        for node in nodes:
            if node.xpath('td/text()')[0].re(u'目前處理程序'):
                item['last_action'] = node.xpath('td/text()').extract()[1]
            if node.xpath('td/text()')[0].re(u'案由'):
                item['abstract'] = node.xpath('td/text()').extract()[1]
            if node.xpath('td/text()')[0].re(u'提案人'):
                item['proposed_by'] = node.xpath('td/div/text()').extract()[0].strip().split(u'、')
            if node.xpath('td/text()')[0].re(u'召集人/委員'):
                item['proposed_by'] = node.xpath('td/text()').extract()[1].strip().split(u'、')
            if node.xpath('td/text()')[0].re(u'議決會次'):
                item['resolusion_date'] = GetDate(node.xpath('td/text()').extract()[1].split()[0])
                item['resolusion_sitting'] = ''.join(node.xpath('td/text()').extract()[1].split()[1:])
            if node.xpath('td/text()')[0].re(u'議決文'):
                item['resolusion'] = node.xpath('td/text()').extract()[1]
            if node.xpath('td/text()')[0].re(u'案(\s|　)+?號'):
                item['bill_no'] = node.xpath('td/text()').extract()[1].strip()
            if node.xpath('td/text()')[0].re(u'來文文號'):
                td = node.xpath('td/text()').extract()[1].split()
                item['intray_date'] = GetDate(td[0])
                if len(td) > 1:
                    item['intray_no'] = td[1]
            if node.xpath('td/text()')[0].re(u'收文日期'):
                item['receipt_date'] = GetDate(node.xpath('td/text()').extract()[1])
            if node.xpath('td/text()')[0].re(u'審查日期'):
                item['examination_date'] = node.xpath('td/text()').extract()[1]
            if node.xpath('td/text()')[0].re(u'審查意見'):
                item['examination'] = '\n'.join(node.xpath('td/text()').extract()[1:])
            if node.xpath('td/text()')[0].re(u'發文文號'):
                td = node.xpath('td/text()').extract()[1].split()
                item['dispatch_date'] = GetDate(td[0])
                if len(td) > 1:
                    item['dispatch_no'] = td[1]
            if node.xpath('td/text()')[0].re(u'執行情形'):
                item['execution'] = node.xpath('td/text()').extract()[1]
            if node.xpath('td/text()')[0].re(u'備[\s]*?註'):
                item['remark'] = '\n'.join(node.xpath('td/text()').extract()[1:])
        item['links'] = response.url
        return item
