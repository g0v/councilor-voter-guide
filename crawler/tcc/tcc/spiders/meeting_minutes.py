# -*- coding: utf-8 -*-
import re
import subprocess
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from tcc.items import MeetingMinutes


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

def take_first(list_in):
    if len(list_in) == 1:
        return list_in[0]
    else:
        raise

class Spider(scrapy.Spider):
    name = "meeting"
    allowed_domains = ["obas_front.tcc.gov.tw"]
    start_urls = ["http://obas_front.tcc.gov.tw:8080/Agenda/EFileSearch.aspx?FileGrpKind=2&h=600",]
    download_delay = 0.5
    payload = {
        '__EVENTTARGET':u'',
        '__EVENTARGUMENT':u'',
        '__LASTFOCUS':u'',
        '__VIEWSTATE':u'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',
        '__EVENTVALIDATION':u'/wEWYALA/pQSAoST4dcPApD4g50OAoDcn8kFAuS+5xUC8vPXwgECu6rhnAQC9ei2wwYCuK6PYQKQt/TRCwLh5bKHBwKK67CcBQLnnfTBAQLPjcGHCALPjcGHCALf4svpBALf4sfpBALA4qvqBALA4qfqBALMk87NBgLc/KigCgLc/KygCgLc/JCgCgLc/JSgCgLc/JigCgLc/JygCgLc/ICgCgLC/OSgCgKX69eQDwK6+qLOBQKo+trPAgLS+9LMDQLnkoWMDgKa7avoDwLRiouaAwKX69uQDwK6+q7OBQKo+tbPAgLS+97MDQLkkoWMDgKZ7avoDwKa7byuAgKln/PuCgKHq+K5AgKN+P+GAgKJo6fzCwLSjKqJAgLHjJaJBQKXr4LUDwK5l6yJAgK8l5iJBQLSufzTDwKUwqaJAgKhwpKJBQL15PbTDwL7yKiJAgL+yJSJBQKQ64DUDwLetbOJAgLbtZ+JBQKr2IPUDwK1vLWJAgLAvKGJBQLW3oXUDwKg466JAgKV45qJBQLphf/TDwL36bCJAgKC6pyJBQKUjInUDwLk6NqABgLp6N6XDAKq19q8BAK779yABgK27+CXDAK13aS9BAKO+N3hDwL2ktnlAwK14fOOCgKx4bePCQLMgOXRDwLD78+/AwLC78+/AwLB78+/AwLA78+/AwLH78+/AwLG78+/AwLF78+/AwLU78+/AwLb78+/AwLD74+8AwLD74O8AwLD74e8AwLD77u8AwLD77+8AwK5ivHKBATOtIbfS2sqzrv8m/DSWeoga05n',
        'btnCongress':u'大會',
        'txtFileName':u'',
        'ddlMeetExpire':u'11',
        'ddlMeetSession':u'',
        'ddlColumn1':u'FileGrpDate',
        'ddlOrder1':u'DESC',
        'ddlColumn2':u'FileGrpNote',
        'ddlOrder2':u'ASC',
        'txtPageSize':u'300',
        'gvEFileList$ctl02$hidFileName':u'',
        'gvEFileList$ctl02$hidFilePath':u'',
        'gvEFileList$ctl02$hidFileGrpKind':u'2',
        'gvEFileList$ctl03$hidFileName':u'',
        'gvEFileList$ctl03$hidFilePath':u'',
        'gvEFileList$ctl03$hidFileGrpKind':u'2',
        'gvEFileList$ctl04$hidFileName':u'',
        'gvEFileList$ctl04$hidFilePath':u'',
        'gvEFileList$ctl04$hidFileGrpKind':u'2',
        'gvEFileList$ctl05$hidFileName':u'',
        'gvEFileList$ctl05$hidFilePath':u'',
        'gvEFileList$ctl05$hidFileGrpKind':u'2',
        'gvEFileList$ctl06$hidFileName':u'',
        'gvEFileList$ctl06$hidFilePath':u'',
        'gvEFileList$ctl06$hidFileGrpKind':u'2',
        'gvEFileList$ctl07$hidFileName':u'',
        'gvEFileList$ctl07$hidFilePath':u'',
        'gvEFileList$ctl07$hidFileGrpKind':u'2',
        'gvEFileList$ctl08$hidFileName':u'',
        'gvEFileList$ctl08$hidFilePath':u'',
        'gvEFileList$ctl08$hidFileGrpKind':u'2',
        'gvEFileList$ctl09$hidFileName':u'',
        'gvEFileList$ctl09$hidFilePath':u'',
        'gvEFileList$ctl09$hidFileGrpKind':u'2',
        'gvEFileList$ctl10$hidFileName':u'',
        'gvEFileList$ctl10$hidFilePath':u'',
        'gvEFileList$ctl10$hidFileGrpKind':u'2',
        'gvEFileList$ctl11$hidFileName':u'',
        'gvEFileList$ctl11$hidFilePath':u'',
        'gvEFileList$ctl11$hidFileGrpKind':u'2',
        'ddlPage':u'1',
        'hFileGrpType':u'大會'
    }

    def start_requests(self):
        return [FormRequest("http://obas_front.tcc.gov.tw:8080/Agenda/EFileSearch.aspx?FileGrpKind=2&h=600", formdata=self.payload, callback=self.parse)]

    def parse(self, response):
        sel = Selector(response)
        nodes = sel.xpath('//table/tr/td/a[contains(@href, "EFileDetail.aspx")]')
        for node in nodes:
            yield Request('http://obas_front.tcc.gov.tw:8080/Agenda/%s' % take_first(node.xpath('@href').extract()), callback=self.parse_profile)

    def parse_profile(self, response):
        sel = Selector(response)
        item = MeetingMinutes()
        item['county'] = u'臺北市'
        nodes = sel.xpath('//table/tbody/tr')
        ref = {
            u'屆別': {'key': 'sitting', 'path': 'td/span/text()'},
            u'類別': {'key': 'category', 'path': 'td/span/text()'},
            u'日期': {'key': 'date', 'path': 'td/span/text()'},
            u'資料名稱': {'key': 'meeting', 'path': 'td/span/text()'},
            u'檔案': {'key': 'download_url', 'path': 'td/a/@href', 'extra': 'http://obas_front.tcc.gov.tw:8080/Agenda/'},
        }
        for node in nodes:
            value = ref.get(take_first(node.xpath('th/text()').re(u'[\s]*([\S]+)[\s]*')))
            if value:
                item[value['key']] = '%s%s' % (value.get('extra', ''), take_first(node.xpath(value['path']).re(u'[\s]*([\S]+)[\s]*')))
        item['date'] = ROC2AD(item['date'])
#       cmd = 'wget -c -O ../../meeting_minutes/tcc/%s_%s.doc %s' % (item['sitting'], item['meeting'], item['download_url'])
#       retcode = subprocess.call(cmd, shell=True)
        return item
