# -*- coding: utf-8 -*-
import os
import re
import time
import subprocess
from datetime import datetime
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from kcc.items import MeetingMinutes


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
    name = "meeting"
    allowed_domains = ["cissearch.kcc.gov.tw"]
    start_urls = ["http://cissearch.kcc.gov.tw/System/MeetingRecord/Default.aspx",]
    download_delay = 0.5
    payload = {
        "ContentPlaceHolder1_ToolkitScriptManager1_HiddenField": "",
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__VIEWSTATE": "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",
        "__EVENTVALIDATION": "WJKJPxVAMQQWg5FTCj4v3zo/e5WCvaf8teq/wQMIk4CSfOaJV9Uf2Ja3tkleifK3z2C2vftw7UXzQ6lKerNH92H28AnyJ/qK5q6uV0kKx0rB+quCaSU9am9g5srKHg3Ag8jwpDPGAJZhUWY4Uh/Mu/D/Ei/ZLbV3EgmcS1/Utwv+6xJq9YYJt/rAoKJ1lent/pJP3qHskTx5DN5rnreAw26eQB4AOHVUjZVf43nAy6u7JJ8JTibXEzbuXnyPUb22VL1Rcqvh+lrdq8yfaIj1FLVPZ/nRhb4hFYCmV5AivBiGzU7MBRTUiG3BZtxWurx3VkDl8lX6mAuMgapteUeRrKiUNIq0aDkgdcCx5hQhN/h9Kr8vq34qAvxB7JL65xZjRYZTeRCh2YGq1p18wlIHB6AI0c8TGqDFidwglkok8g5AC9V4YBUuovVDEQ23TdmFvM51D9gnTNbmZzmciCQHc0aE9/Qj9BxhZwtL26G6lMygDH06G6XUqkkGJFoG+VegO2BXIX8occ0Bm6v4/qMmuYok4Dy29tkSahe5KWQOCRmcjV3gLb+T15qaj8sMU7zZdWgAYzsl7m35OTiTqr0bDtZB9bGHfJfhYarFkcDU3BCfDO9z2/J9dKPLLfkZ6OSYVwh66eAI4oS5PFsJOjDMBwHN602D7Rm2Xzv4Th4Fl/ac1hDJ//cBfgeTVZ/cVhsLu29bfdSHyqDxUy1O80nYL6X5b+XVn22tyJm02V1ZdFZ01AqKZL6negtvXNR83IYVLEgsjLsnsOpThiRbGeYZIAu9YZI594SXiadLOEY8SYKyZh0AaKKGrh4t3n2pDK90Sv83Ol4lW0TMg9ZVgi6rFCfOH/neAvZq4xQD9LYj/zfMqdeYnMBzJ90Xmgt0TlHze2gYRGKjQxaCpqXQlKw8iaIDHUS28i5NgvejM8tpd3U=",
        "__VIEWSTATEENCRYPTED": "",
        "ctl00$txtKeyword": "",
        "ctl00$ContentPlaceHolder1$hidCurrentTab": "",
        "ctl00$ContentPlaceHolder1$SearchSelect": "rad02",
        "ctl00$ContentPlaceHolder1$uscDateTimeStart$txtDateTime": "98-12-25",
        "ctl00$ContentPlaceHolder1$uscDateTimeEnd$txtDateTime": "%d-%d-%d" % (datetime.now().year - 1911, datetime.now().month, datetime.now().day)
    }

    def start_requests(self):
        return [FormRequest("http://cissearch.kcc.gov.tw/System/MeetingRecord/Default.aspx", formdata=self.payload, callback=self.parse)]

    def parse(self, response):
        sel = Selector(response)
        count = sel.xpath('//span[@id="ContentPlaceHolder1_DataPager1"]/text()').re(u'共\s*(\d+)\s*筆')[0]
        print count
        payload = self.payload.copy()
        payload["ctl00$ContentPlaceHolder1$DataPager1$ctl02$txtPageSize"] = count
        payload["ctl00$ContentPlaceHolder1$btnGo"] = " Go "
        yield FormRequest("http://cissearch.kcc.gov.tw/System/MeetingRecord/Default.aspx", formdata=payload, callback=self.parse_profile, dont_filter=True)

    def parse_profile(self, response):
        sel = Selector(response)
        trs = sel.xpath('//table[@id="ContentPlaceHolder1_gvIndex"]/tr')
        items = []
        for tr in trs:
            item = MeetingMinutes()
            tds = tr.xpath('td')
            if tds:
                item['county'] = u'高雄市'
                item['date'] = ROC2AD(tds[1].xpath('text()').extract()[0])
                item['meeting'] = tds[2].xpath('text()').extract()[0].strip()
                item['download_url'] = "http://cissearch.kcc.gov.tw%s" % tds[3].xpath('a/@href').extract()[0].strip()
                file_name = item['download_url'].split('/')[-1]
                items.append(item)
                if os.path.exists('../../meeting_minutes/kcc/%s' % file_name):
                    continue
                cmd = 'wget -c -O ../../meeting_minutes/kcc/%s %s' % (file_name, item['download_url'])
                retcode = subprocess.call(cmd, shell=True)
                time.sleep(1)
        return items
