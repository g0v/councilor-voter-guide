# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Councilor(Item):
    name = Field()
    ad = Field()
    gender = Field()
    birth = Field()
    party = Field()
    constituency = Field()
    county = Field()
    district = Field()
    contacts = Field()
    education = Field()
    experience = Field()
    platform = Field()
    remark = Field()
    image = Field()
    url = Field()

class Taipei(Item):
    sitting = Field()
    category = Field()
    date = Field()
    meeting = Field()
    download_url = Field()
