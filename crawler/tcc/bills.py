# -*- coding: utf-8 -*-
import re
import urllib
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from tcc.items import Bills


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
    allowed_domains = ["tccmis.tcc.gov.tw"]
    start_urls = ["http://tccmis.tcc.gov.tw/OM/OM_SearchList.asp",]
    election_year = {1: '1969', 2: '1973', 3: '1977', 4: '1981', 5: '1985', 6: '1989', 7: '1994', 8: '1998', 9: '2002', 10: '2006', 11: '2010', 12: '2014'}
    select_ad = 11
    download_delay = 0.5

    def start_requests(self):
        payload = {
            'FTSearch': u'ON',
            'pagesize': u'20',
            'omastext': u'',
            'rdoDE': u'0',
            'OmasDetr': str(self.select_ad),
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
            item['election_year'] = self.election_year[self.select_ad]
            item['county'] = u'臺北市'
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
                council_motion['date'] = ROC2AD(node.xpath('td/text()').extract()[1].split()[0])
                council_motion['sitting'] = ''.join(node.xpath('td/text()').extract()[1].split()[1:])
            elif node.xpath('td/text()')[0].re(u'議決文'):
                council_motion['resolusion'] = node.xpath('td/text()').extract()[1]
            elif node.xpath('td/text()')[0].re(u'案(\s|　)+?號'):
                item['bill_no'] = node.xpath('td/text()').extract()[1].strip()
            elif node.xpath('td/text()')[0].re(u'來文文號'):
                td = node.xpath('td/text()').extract()[1].split()
                d = dict(zip(['motion', 'resolution', 'date'], [u'來文', None, ROC2AD(td[0])]))
                if len(td) > 1:
                    d['no'] = td[1]
                motions.append(d)
            elif node.xpath('td/text()')[0].re(u'收文日期'):
                motions.append(dict(zip(['motion', 'resolution', 'date'], [u'收文', None, ROC2AD(node.xpath('td/text()').extract()[1])])))
            elif node.xpath('td/text()')[0].re(u'審查日期'):
                committee_motion['motion'] = u'委員會審查意見'
                committee_motion['date'] = node.xpath('td/text()').extract()[1]
            elif node.xpath('td/text()')[0].re(u'審查意見'):
                committee_motion['resolution'] = '\n'.join(node.xpath('td/text()').extract()[1:])
            elif node.xpath('td/text()')[0].re(u'發文文號'):
                td = node.xpath('td/text()').extract()[1].split()
                d = dict(zip(['motion', 'resolution', 'date'], [u'發文', None, ROC2AD(td[0])]))
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
        item['motions'] = motions
        item['links'] = response.url
        return item
