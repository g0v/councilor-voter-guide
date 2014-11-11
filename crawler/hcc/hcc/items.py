# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class Councilor(Item):
    # define the fields for your item here like:
    name = Field()
    county = Field()
    district = Field()
    education = Field()
    experience = Field()
    image = Field()
    links = Field()
    platform = Field()
    party = Field()
    contact_details = Field()
