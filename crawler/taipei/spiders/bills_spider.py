# -*- coding: utf-8 -*-
import re
import urllib
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from taipei.items import Bills


def take_first(list_in):
    if len(list_in) == 1:
        return list_in[0]
    else:
        raise

class Spider(BaseSpider):
    #for scrapy
    name = "taipei_bills"
    allowed_domains = ["tccmis.tcc.gov.tw"]
    start_urls = ["http://tccmis.tcc.gov.tw/OM/OM_SearchList.asp",]
    def start_requests(self):
        payload = {
            'FTSearch': u'ON',
            'pagesize': u'20',
            'omastext': u'',
            'rdoDE': u'0',
            'OmasDetr': u'11',
            'OmasDetp': u'0',
            'OmasDetm': u'01',
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
        items = []
        sel = Selector(response)
        nodes = sel.xpath('//div/table/tr[@id="tr"]')
        for node in nodes:
            item = Bills()
            td = nodes.xpath('td/text()').extract()
            item['id'] = td[2].encode('latin1').decode('big5')
            item['type'] = td[3].encode('latin1').decode('big5')
            request = Request('%s%s' % ("http://tccmis.tcc.gov.tw/OM/OM_SearchDetail.asp?sys_no=", item['id']), callback=self.parse_profile)
            request.meta['item'] = item
            yield request

    def parse_profile(self, response):
        sel = Selector(response)
        return item
