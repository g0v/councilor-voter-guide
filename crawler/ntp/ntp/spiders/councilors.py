# -*- coding: utf-8 -*-
import os
import json
import urllib
from urlparse import urljoin

import scrapy
from scrapy import log

from ntcc.items import Councilor

def extract(elem, xpath, default=''):
    ## some ditry work here
    try:
        return elem.xpath(xpath).extract()[0]
    except:
        log.msg("Extracted empty field: %s" % xpath,
                _level=log.WARNING
                )
        return default

class Spider(scrapy.Spider):
    name = 'councilors'
    start_urls = []

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'constituency.json'), 'r') as fh:
            self.constituency = json.loads(fh.read())

    def start_requests(self):
        self.url_root = "http://www.ntp.gov.tw/content/list"
        self.url_list = "list02.aspx"

        yield scrapy.Request("%s/%s" % (self.url_root, self.url_list))

    def parse(self, response):
        xp_details = \
            '//*[@id="main"]/table/tr/td/table/tr[4]/td/table[1]/tr[2]/td[2]/table/tr/td[2]/a/@href'
        elem_details = response.xpath(xp_details)
        #log.msg("=== %s " % elem_details.extract())

        for url in elem_details.extract():
            yield scrapy.Request('%s/%s' % (self.url_root, url),
                    callback=self.parse_profile
                    )

    def parse_profile(self, response):
        c = Councilor()
        res = response

        xp_photo = \
            '//*[@id="main"]/table/tr/td/table/tr[1]/td/table/tr/td[2]/img/@src'
        elem_photo = response.xpath(xp_photo)

        c['image'] = urljoin(response.url,
                urllib.quote(extract(res, xp_photo, '').encode('utf8'))
                )
        c['links'] = [{'url': response.url, 'note': u'議會個人官網'}]

        xp_const = \
            '//*[@id="printContext"]/table[1]/tr/td[2]/table/tr[1]/td/a[4]/text()'
        c['constituency'] = extract(res, xp_const, '')
        ## TODO: some newer extraction?
        c['county'] = u'新北市'
        ## TODO: further extraction here
        log.msg(self.constituency)
        c['district'] = self.constituency[c['constituency']]

        c['contact_details'] = []
        xp_profile = \
            '//*[@id="main"]/table/tr/td/table/tr[1]/td/table/tr/td[3]/table[2]/tr/td[1]/table[1]/tr'
        elem_profile = response.xpath(xp_profile)

        prof_mappings = {
                ## 0: assign
                ## 1: append to contacts
                ## 2: append
                u'姓名': ('name', '/text()', 0),
                u'政黨': ('party','/text()', 0),
                u'電話': ('voice', '/text()', 1),
                u'傳真': ('fax', '/text()', 1),
                u'通訊處': ('address', '/text()', 1),
                u'E-mail': ('email', '/a/text()', 1),
                u'網站連結': ('links', '/a/@href', 2)
                }

        for elem in elem_profile:
            k = extract(elem, 'td[2]/text()', '')
            #v = extract(elem, 'td[3]/text()', '')
            if not k:
                continue
            else:
                for prof_item in prof_mappings.keys():
                    if k.startswith(prof_item):
                        prop, xp_add, process = prof_mappings[prof_item]
                        v = extract(elem, 'td[3]%s' % xp_add, '')

                        if process == 0:
                            c[prop] = v
                        elif process == 1:
                            c['contact_details'].append({
                                'label': prof_item,
                                'type': prop,
                                'value': v
                                })
                        elif process == 2:
                            ## for links only
                            c[prop].append({
                                'note': u'個人網站',
                                'url': v
                                })
                        else:
                            pass

        c['education'] = [x.strip() for x in response.xpath(u'//img[@alt="學歷"]/../../following-sibling::tr[1]/td/table/tr/td/text()').extract()]
        c['experience'] = [x.strip() for x in response.xpath(u'//img[@alt="經歷"]/../../following-sibling::tr[1]/td/table/tr/td/text()').extract()]
        c['title'] = response.xpath(u'//img[@alt="現任"]/../../following-sibling::tr[1]/td/table/tr/td/text()').re(u'第\d+屆(.+)')[0]
        c['platform'] = [x.strip() for x in response.xpath(u'//img[@alt="政見"]/../../following-sibling::tr[1]/td/table/tr/td/div/table/tr/td/text()').extract()]

        ## some dirty hand items
        c['election_year'] = '2010'
        c['in_office'] = True
        c['term_start'] = '%s-12-25' % c['election_year']
        c['term_end'] = {'date': '2014-12-24'}

        yield c
