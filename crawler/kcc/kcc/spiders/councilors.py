# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from kcc.items import Councilor


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
        sel = Selector(response)
        nodes = sel.xpath('//map[@id="imgsmapMap"]/area')
        items = []
        for node in nodes:
            constituency = node.xpath('@title').re(u"連結至(第\d+選區)")[0]
            area_id = node.xpath('@href').re(u'#(.+)')[0]
            area_node = sel.xpath('//table/tr/td/div/div/a[@id="%s"]' % area_id)[0]
            district = u'、'.join(area_node.xpath('../../../div/ul[@class="all_area"]/li/text()').extract())
            print district
            for name in area_node.xpath('../../../div/ul[@class="embers_mame"]/li/a/text()').extract():
                item = Councilor()
                item['election_year'] = '2010'
                item['county'] = '高雄市'
                item['name'] = re.sub(u'\(.*\)', '', name)
                item['constituency'] = constituency
                item['district'] = district
                items.append(item)
                print item
        return items
