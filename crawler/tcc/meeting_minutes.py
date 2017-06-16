# -*- coding: utf-8 -*-
import re
import subprocess
from urlparse import urljoin
import scrapy


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
        'btnCongress': u'大會',
        'txtPageSize': u'300',
    }

    def parse(self, response):
        return scrapy.FormRequest.from_response(response, response.url, formdata=self.payload, callback=self.parse_post)

    def parse_post(self, response):
        links = response.xpath('//table/tr/td/a[contains(@href, "EFileDetail.aspx")]/@href').extract()
        for link in links:
            yield scrapy.Request(urljoin(response.url, link), callback=self.parse_profile)

    def parse_profile(self, response):
        item = {}
        item['election_year'] = '2014'
        nodes = response.xpath('//table/tbody/tr')
        ref = {
            u'屆別': {'key': 'sitting', 'path': 'td/span/text()'},
            u'類別': {'key': 'category', 'path': 'td/span/text()'},
            u'日期': {'key': 'date', 'path': 'td/span/text()'},
            u'資料名稱': {'key': 'meeting', 'path': 'td/span/text()'},
            u'檔案': {'key': 'download_url', 'path': 'td/a/@href', 'extra': 'http://obas_front.tcc.gov.tw:8080/Agenda/'},
        }
        for node in nodes:
            value = ref.get(node.xpath('th/text()').extract_first().strip())
            if value:
                item[value['key']] = '%s%s' % (value.get('extra', ''), node.xpath(value['path']).extract_first())
        item['date'] = ROC2AD(item['date'])
        ext = re.search(u'FileName=[\w\d]+\.(\w+)&', item['download_url']).group(1)
        item['file_name'] = '%s_%s.%s' % (item['sitting'], item['meeting'], ext)
        output_path = '../../meeting_minutes/tcc/%s/' % item['election_year']
        cmd = 'mkdir -p %s && wget -c -O %s%s "%s"' % (output_path, output_path, item['file_name'], item['download_url'])
        retcode = subprocess.call(cmd, shell=True)
        return item
