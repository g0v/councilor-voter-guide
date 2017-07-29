# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
import scrapy
from urlparse import urljoin

import common


class Spider(scrapy.Spider):
    name = "bills"
    handle_httpstatus_list = [302]
    allowed_domains = ["kcc.gov.tw"]
    start_urls = ["http://www.kcc.gov.tw",]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    ads = {'2010': u'一', '2014': u'二', '2018': u'三'}
    ad = ads[election_year]

    def parse(self, response):
        return response.follow(response.xpath(u'//a[re:test(., "^大會提案$")]/@href').extract_first(), callback=self.parse_query)

    def parse_query(self, response):
        payload = {
            'ctl00$ContentPlaceHolder1$uscPeriodSessionMeeting$ddlSession': response.xpath(u'//select[@name="ctl00$ContentPlaceHolder1$uscPeriodSessionMeeting$ddlSession"]/option[re:test(., "%s屆")]/@value' % self.ad).extract_first(),
            'ctl00$ContentPlaceHolder1$uscPeriodSessionMeeting$ddlMeeting': '',
            '__EVENTTARGET': re.search('_PostBackOptions\("([^"]*)', response.css('#ContentPlaceHolder1_LinkButton1::attr(href)').extract_first()).group(1)
        }
        yield scrapy.FormRequest.from_response(response, formdata=payload, callback=self.parse_type, dont_filter=True, dont_click=True, headers=common.headers(self.county_abbr))

    def parse_type(self, response):
        tabs = response.xpath('//div[@id="tabs"]/ul/li/a')
        for i, tab in enumerate(tabs, 1):
            type, count = tab.xpath('text()').extract()
            count = re.sub('\D', '', count)
            if count:
                payload = {"ctl00$ContentPlaceHolder1$DataPager%d$ctl02$txtPageSize" % i: count}
                if i != 1:
                    payload["ctl00$ContentPlaceHolder1$btnGo%d" % i] = " Go "
                else:
                    payload["ctl00$ContentPlaceHolder1$btnGo"] = " Go "
                yield scrapy.FormRequest.from_response(response, formdata=payload, callback=self.parse_tab, dont_filter=True, meta={'type': tab.xpath('text()').extract_first().strip(), 'tab_id': 'tabs-%d' % i})

    def parse_tab(self, response):
        trs = response.xpath('//div[@id="%s"]/div/table/tr[count(td)>1]' % response.meta['tab_id'])
        for tr in trs:
            item = {}
            item['election_year'] = self.election_year
            item['type'] = response.meta['type']
            item['last_action'] = tr.xpath('td[6]/text()').extract_first()
            link = tr.xpath('td[@onclick]/@onclick').re(u"\.href='([^']+)'")[0]
            yield response.follow(link, callback=self.parse_profile, meta={'dont_redirect': True, 'item': item})

    def parse_profile(self, response):
        item = response.meta['item']
        item['id'] = '-'.join(re.findall(u'=([^&]*)', response.url))
        for key, label in [('category', u'類別'), ('abstract', u'案由'), ('description', u'說明'), ('methods', u'辦法'), ('remark', u'備註'), ]:
            content = response.xpath(u'string((//td[re:test(., "%s")]/following-sibling::td)[1])' % label).extract_first()
            if content:
                item[key] = content.strip()
        item['proposed_by'] = re.split(u'\s|、', re.sub(u'(副?議長|議員)', '', response.xpath(u'(//td[re:test(., "提案(人|單位)")]/following-sibling::td)[1]/text()').extract_first()).strip())
        item['petitioned_by'] = re.split(u'\s|、', re.sub(u'(副?議長|議員)', '', (response.xpath(u'(//td[re:test(., "連署人")]/following-sibling::td)[1]/text()').extract_first() or '')).strip())
        item['motions'] = []
        for motion in [u'一讀', u'委員會審查意見', u'二讀決議', u'三讀決議', ]:
            date = common.ROC2AD(''.join(response.xpath(u'(//td[re:test(., "%s")]/following-sibling::td)[1]/span/text()' % motion).extract()))
            resolution = ''.join([x.strip() for x in response.xpath(u'(//td[re:test(., "%s")]/following-sibling::td)[1]/text()' % motion).extract()])
            if date or resolution:
                item['motions'].append(dict(zip(['motion', 'resolution', 'date'], [motion, resolution, date])))
        item['links'] = [
            {
                'url': response.url,
                'note': 'original'
            }
        ]
        return item
