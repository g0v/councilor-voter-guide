# -*- coding: utf-8 -*-
import re
import urllib
import codecs
import subprocess
from urlparse import urljoin
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from ..items import MeetingMinutes


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

def write_file(data, file_name):
    file = codecs.open(file_name, 'w', encoding='utf-8')
    file.write(data)
    file.close()

class Spider(scrapy.Spider):
    name = "meeting"
    allowed_domains = ["www.ntp.gov.tw"]
    start_urls = ['http://www.ntp.gov.tw/content/information/information04.aspx']
    download_delay = 1

    def parse(self, response):
        for node in response.xpath(u'//a[contains(@title, "HTML檔")]/@href').extract():
            yield Request(node, callback=self.parse_sitting)

    def parse_sitting(self, response):
        for node in response.xpath(u'//a/@href').extract():
            yield Request(urljoin(response.url, node), callback=self.parse_meeting)

    def parse_meeting(self, response):
        sitting = response.xpath('//head/title/text()').re(u'(.+)日程表')[0]
        trs = [tr for tr in response.xpath('//table/tr') if tr.xpath('td[3]/text()').re('\d+')]
        for tr in trs:
            item = MeetingMinutes()
            item['county'] = u'新北市'
            item['date'] = ROC2AD(tr.xpath('td[1]/text()').extract()[0])
            item['sitting'] = sitting
            item['meeting'] = tr.xpath('td[3]/text()').extract()[0]
            item['download_url'] = urljoin(response.url, tr.xpath('td[6]/a[1]/@href').extract()[0])
            if re.search('\.pdf$', item['download_url']):
                yield Request(item['download_url'], callback=self.download_pdf, meta={'item': item})
            elif re.search('\.htm$', item['download_url']):
                yield Request(item['download_url'], callback=self.parse_html, meta={'item': item})

    def download_pdf(self, response):
        item = response.meta['item']
        cmd = 'wget -c -O ../../meeting_minutes/ntcc/%s_%s.pdf %s' % (item['sitting'], item['meeting'], item['download_url'])
        retcode = subprocess.call(cmd, shell=True)
        return item

    def parse_html(self, response):
        item = response.meta['item']
        print '%s_%s' % (item['sitting'], item['meeting'])
        text = '\n'.join(response.xpath('//pre/text()').extract())
        write_file(text, '../../meeting_minutes/ntcc/%s_%s.txt' % (item['sitting'], item['meeting']))
        return item
