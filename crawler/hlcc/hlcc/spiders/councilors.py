# -*- coding: utf-8 -*-
import re
import urllib
from urlparse import urljoin
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from hlcc.items import Councilor
import logging


class FieldHandler(object):
    def __init__(self, field_name, wrapper=None, default_value=None):
        self.field_name = field_name
        self.wrapper = wrapper
        self.default_value = default_value

    def fill_field(self, item, value):
        if self.wrapper:
            value = self.wrapper(value)

        if not value and self.default_value:
            value = self.default_value

        item[self.field_name] = value

        return item


class ListFieldHandler(FieldHandler):

    def fill_field(self, item, value):
        if self.wrapper:
            value = self.wrapper(value)

        if self.field_name not in item:
            item[self.field_name] = []

        item[self.field_name].append(value)

        return item

def split_orz_format(value):
    # If there is only 1 value, try to split the value by 、(\u3001)|，(\uff0c)|。(\u3002),
    # Because format is not consistent
    if len(value) == 1:
        tmp = value[0].strip()

        split_token = None

        if u"\uff0c" in tmp:
            split_token = u"\uff0c"
        elif u"\u3002" in tmp and (not tmp.endswith(u"\u3002") if tmp.count(u"\u3002") == 1 else True):
            split_token = u"\u3002"
        else:
            split_token = u"\u3001"

        value = tmp.split(split_token)

    return [item.strip() for item in value]

def text(value):
    value = map(lambda item: item.strip(), value)
    return "".join(value)


class Spider(scrapy.Spider):
    name = "councilors"
    allowed_domains = ["www.hlcc.gov.tw"]
    start_urls = ["http://www.hlcc.gov.tw/councillor.php", ]
    
    download_delay = 0.5

    ROOT_URL = "http://www.hlcc.gov.tw/"

    handler_map = {
        u"性別": FieldHandler("gender", text),
        u"黨籍": FieldHandler("party", text, u"無黨籍"),
        u"出生地": None,
        u"學歷": FieldHandler("education", split_orz_format),
        u"經歷": FieldHandler("experience", split_orz_format),

        # contact_details
        u"服務處地址": ListFieldHandler("contact_details",
            lambda value: {"type": "address", "label": u"通訊處", "value": text(value)}),
        u"聯絡電話": ListFieldHandler("contact_details",
            lambda value: {"type": "voice", "label": u"電話", "value": text(value)}),
    }

    def parse(self, response):
        sel = Selector(response)
        areas = sel.xpath('//div[contains(@class, "area-2")]/table')

        for area in areas:
            area_info = area.xpath('tr[1]//td[@valign="middle"]/div[@align="center"]/font')

            if area_info:
                constituency = area_info[0].xpath("text()").extract()[0]
                district = u"\u3001".join(area_info[1].xpath("text()").extract())
                councilors = self.__parse_councilor_base_info(area)

                for name, url in councilors:
                    yield Request(self.ROOT_URL + url,
                                  meta={
                                      "constituency": constituency,
                                      "district": district,
                                      "name": name
                                  },
                                  callback=self.parse_councilor_profile)

    def __parse_councilor_base_info(self, area):
        base_info_list = area.xpath('tr[2]//span[@class="td-content"]')

        for base_info in base_info_list:
            name = base_info.xpath("text()").extract()[0].strip()
            url = base_info.xpath('a/@onclick').re("(councillor-data.php\?index_no=[\d]+)")[0]
            yield name, url

    def parse_councilor_profile(self, response):
        sel = Selector(response)

        item = Councilor()

        # Default value
        item['election_year'] = '2010'
        item['in_office'] = True

        # Save response metadata

        item["name"] = response.meta["name"]
        item["district"] = response.meta["district"]
        item["constituency"] = response.meta["constituency"]

        # Parse profile
        rows = sel.xpath('//body/table/tr')

        item["image"] = self.ROOT_URL + sel.xpath('//body/table//img/@src').extract()[0]

        for row in rows:
            field = row.xpath('td[@class="style3"]')

            field_name = field[0].xpath("div/text()").extract()[0]
            field_value = field[1].xpath("text()").extract()

            handler = self.handler_map.get(field_name)

            if handler:
                item = handler.fill_field(item, field_value)

        return item

