# -*- coding: utf-8 -*-
import re
import urllib
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from ntc.items import Bills
from crawler_lib import parse
from crawler_lib import misc
from scrapy.utils.url import canonicalize_url



class Spider(scrapy.Spider):
    name = "bills"
    #allowed_domains = ["www.ntcc.gov.tw"]
    #start_urls = ["http://www.ntcc.gov.tw/ntcc/anews_list_show.asp?sn=20140901141308",]
    election_year = {2009}
    f = open("url.txt")
    start_urls = [url.strip() for url in f.readlines()]
    download_delay = 0.5
    f.close()


    def parse(self, response):
        response = parse.get_decoded_response(response, 'big5')
        sel = Selector(response)
        items = []
        item = Bills()
        nodes = sel.xpath('//table/tr')
        item['election_year'] = '2009'
        item['county'] = u'南投縣'


        extract_result = nodes.xpath('td[2]/text()').extract()

        

        item['proposed_by'] = extract_result[0].strip().split(u'、')
        item['petitioned_by'] = extract_result[1].replace(u'議長','').strip().split(u'、')
        item['abstract'] = extract_result[2].strip()
        item['description'] = extract_result[3].strip()
        item['methods'] = extract_result[4].strip()
        value = extract_result[5].strip()
        item['category'] = value[0:2]
        item['motions'] = []
        item['motions'].append({"motion": u'審查意見', "resolution": extract_result[6]})
        item['motions'].append({"motion": u'大會決議', "resolution": extract_result[7]})
        item['last_action'] = extract_result[8].strip()
        item['remark'] = extract_result[9].strip()
        item['links'] = response.url

        return item
