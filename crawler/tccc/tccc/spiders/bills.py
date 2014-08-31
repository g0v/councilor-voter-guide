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

        rows = sel.xpath('//*[@id="block"]/table//tr')
        dic = {}
        for row in rows:
            cols = [
                ' '.join([txt.strip() for txt in col.xpath('text()').extract()])
                for col in row.xpath('td')]
            for i in range(0, len(cols), 2):
                if i + 1 >= len(cols):
                    break

                k = cols[i]
                v = cols[i + 1]

                if k:
                    dic[k] = v

        cate = dic.pop(u'審查會別 議案類別', None)
        if cate:
            cates = cate.split(' ')
            dic[u'審查會別'] = cates[0]
            dic[u'議案類別'] = cates[1]

        item = Bills()

        field_map = {
            u"案由": {'name': 'abstract'},
            u"案號": {'name': 'bill_no'},
            u"議案類別": {'name': 'category'},
            u"連署人": {'name': 'petitioned_by'},
            u"會次": {'name': 'resolusion_sitting'},
            u"提案人": {'name': 'proposed_by'},
            u"大會意見": {'name': 'resolusion'},
            u"辦理情形": {'name': 'execution'},
            # u"理由": {'name': ''},
            # u"審查會別": {'name': ''},
            # u"分組審查意見": {'name': ''},
            # u"地址": {'name': ''},
            # u"工務建設委員會": {'name': ''},
            # u"提案單位": {'name': ''},
            # u"辦法": {'name': ''},
        }

        others = {}
        for k_chinese, v in dic.iteritems():
            info = field_map.get(k_chinese)
            if info:
                k = info['name']
                item[k] = v
            else:
                others[k_chinese] = v

        item['others'] = others
        item['links'] = response.url

        return item
