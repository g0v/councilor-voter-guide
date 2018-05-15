# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
import json
import time
import scrapy

import common


class Spider(scrapy.Spider):
    name = "bills"
    allowed_domains = ["tpa.gov.tw", ]
    start_urls = ["http://mtcc.digital.tpa.gov.tw/"]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    election_year = common.election_year(county_abbr)
    ads = {'2009': u'連江縣.*?第(五|5)屆', '2014': u'連江縣.*?第(六|6)屆', '2018': u'連江縣.*?第(七|7)屆'}
    ad = ads[election_year]

    def parse(self, response):
        return response.follow('/index.php?act=GuestLogin', callback=self.parse_login)

    def parse_login(self, response):
        return response.follow(response.xpath(u'//a[re:test(., "^提案$")]/@href').extract_first(), callback=self.parse_unordered, headers=common.headers(self.county_abbr))

    def parse_unordered(self, response):
        payload = {
            'act': 'search_set',
            'field': 'SET_OrderByMethod',
            'value': 'DESC'
        }
        yield scrapy.FormRequest(response.urljoin('application.php'), formdata=payload, callback=self.parse_reload, meta={'url': response.url}, headers=common.headers(self.county_abbr))

    def parse_reload(self, response):
        return response.follow(response.meta['url'], callback=self.parse_query, dont_filter=True, headers=common.headers(self.county_abbr))

    def parse_query(self, response):
        pages = re.sub('\D', '', response.css('.result_select').xpath('string()').extract_first())
        for node in response.css('.result_content'):
            link_node = node.css('.acc_link a')
            if link_node.xpath('text()').re(self.ad):
                item = {}
                item['election_year'] = self.election_year
                link = link_node.xpath('@href').extract_first()
                item['id'] = node.css('.acc_type::text').extract_first().split('@')[0].strip()
                level = node.xpath(u'string((descendant::span[re:test(., "類別階層")]/following-sibling::span)[1])').extract_first()
                item['type'], item['category'] = re.search(u'/([^/]+)/?(.*)$', level).groups()
                item['abstract'] = re.sub('\s', '', node.css('.result_text::text').extract_first())
                yield response.follow(link, callback=self.parse_profile, meta={'item': item, 'handle_httpstatus_list': [302], 'dont_redirect': True}, headers=common.headers(self.county_abbr))
            else:
                raise scrapy.exceptions.CloseSpider('out of date range')
            time.sleep(.5)
        next_page = response.css('.page_botton.pb_pagedw::attr(href)').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse_query)

    def parse_profile(self, response):
        try:
            payload = {
                'act': 'act_initial',
                'target': re.search('=([^&]*)', response.headers['Location']).group(1),
                'refer': 'serial'
            }
        except:
            print response.headers
            print response.body
            print response.status
            print response.url
            print 'profile:', response.urljoin(response.headers['Location'])
            raise scrapy.exceptions.CloseSpider('no redirect location')
        yield scrapy.FormRequest(response.urljoin(response.headers['Location']), formdata=payload, callback=self.parse_post, meta={'item': response.meta['item']})

    def parse_post(self, response):
        item = response.meta['item']
        try:
            jr = json.loads(response.body_as_unicode())['data']['meta'][0]
        except:
            print 'no json response:', response.url
            raise scrapy.exceptions.CloseSpider('no json response')
        item['proposed_by'] = re.sub(u'(副?議長|議員)', '', jr.get('Member') or jr.get('Organ') or jr.get('OrganPetiti') or jr.get('Chairman') or jr.get('Council')).strip().split(u'，')
        if not item['proposed_by'][0]:
            print jr
            raise scrapy.exceptions.CloseSpider('empty proposed_by')
        item['petitioned_by'] = re.sub(u'(副?議長|議員)', '', (jr.get('MemberRelated') or jr.get('OrganPetiti') or '')).strip().split(u'，')
        item['links'] = [
            {
                'url': response.url,
                'note': 'original'
            }
        ]
        return item
