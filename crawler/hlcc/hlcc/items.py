# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Councilor(Item):
    name = Field()
    stage = Field()
    election_year = Field()
    title = Field()
    gender = Field()
    birth = Field()
    party = Field()
    constituency = Field()
    county = Field()
    district = Field()
    contact_details = Field()
    education = Field()
    experience = Field()
    platform = Field()
    remark = Field()
    in_office = Field()
    term_end = Field()
    term_start = Field()
    image = Field()
    links = Field()
