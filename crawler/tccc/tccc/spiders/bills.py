# -*- coding: utf-8 -*-
import re
import urllib
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from tccc.items import Bills


class Spider(scrapy.Spider):
    name = "bills"
    # allowed_domains = ["163.29.76.77"]
    base_url = "http://163.29.76.77"
    start_urls = ["http://163.29.76.77/tccc/jsp/b_0.jsp", ]
    download_delay = 0.5

    def start_requests(self):
        payload = {
            "time": "",
            "committee": "0",
            "source": "0",
            "billtype": "0",
            "no": "",
            "originator": "",
            "second": "",
            "subject": "",
            "Submit1": "查詢",
        }
        return [FormRequest(self.start_urls[0], formdata=payload, callback=self.parse)]

    def parse(self, response):
        sel = Selector(response)
        rows = sel.xpath('//*[@id="form1"]/table//tr')
        for row in rows:
            onclick = row.xpath('.//input/@onclick').extract()
            if not onclick:
                continue

            onclick = onclick[0]
            m = re.match(r".*open\('([^']*)',.*\).*", onclick)
            if not m:
                continue

            url = self.base_url + m.group(1)

            request = Request(url, callback=self.parse_profile)
            yield request

    def parse_profile(self, response):
        sel = Selector(response)
        item = Bills()
        item['election_year'] = u'2010'
        item['county'] = u'臺中市'
        item['id'] = '-'.join(re.findall(u'=(\d+)', response.url))
        item['links'] = response.url
        trs = sel.xpath('//*[@id="block"]/table//tr')
        motions = []
        for tr in trs:
            tds = tr.xpath('td')
            for i in range(0, len(tds), 2):
                if tds[i].xpath('text()').re(u'會次'):
                    item['resolusion_sitting'] = tds[i+1].xpath('text()').extract()[0].strip()
                elif tds[i].xpath('text()').re(u'審查會別'):
                    item['committee'] = tds[i+1].xpath('text()').extract()[0].strip()
                    item['category'] = tds[i+1].xpath('text()').extract()[1].strip()
                elif tds[i].xpath('text()').re(u'提案人'):
                    item['proposed_by'] = tds[i+1].xpath('text()').extract()[0].strip().split(u'、')
                elif tds[i].xpath('text()').re(u'連署人'):
                    item['petitioned_by'] = tds[i+1].xpath('text()').extract()[0].strip().split(u'、')
                elif tds[i].xpath('text()').re(u'案號'):
                    item['bill_no'] = tds[i+1].xpath('text()').extract()[0].strip()
                elif tds[i].xpath('text()').re(u'案由'):
                    item['abstract'] = tds[i+1].xpath('text()').extract()[0].strip()
                elif tds[i].xpath('text()').re(u'理由'):
                    item['description'] = '\n'.join([x.strip() for x in tds[i+1].xpath('text() | p/text()').extract()])
                elif tds[i].xpath('text()').re(u'辦法'):
                    item['methods'] = '\n'.join([x.strip() for x in tds[i+1].xpath('text() | p/text()').extract()])
                elif tds[i].xpath('text()').re(u'分組審查意見'):
                    motions.append(dict(zip(['motion', 'resolution', 'date'], [u'分組審查意見', '\n'.join([x.strip() for x in tds[i+1].xpath('text() | div/font/text() | p/span/text()').extract()]), None])))
                elif tds[i].xpath('text()').re(u'大會意見'):
                    motions.append(dict(zip(['motion', 'resolution', 'date'], [u'大會意見', '\n'.join([x.strip() for x in tds[i+1].xpath('text() | p/text()').extract()]), None])))
                elif tds[i].xpath('text()').re(u'辦理情形'):
                    item['execution'] = '\n'.join([x.strip() for x in tds[i+1].xpath('text() | p/text()').extract()])
        item['motions'] = motions
        return item
