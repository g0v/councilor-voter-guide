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
    links = Field()

class Bills(Item):
    id = Field()
    type = Field()
    category = Field()
    abstract = Field()
    proposed_by = Field()
    resolusion = Field()
    resolusion_sitting = Field()
    resolusion_date = Field()
    last_action = Field()
    abstract = Field()

class MeetingMinutes(Item):
    sitting = Field()
    category = Field()
    date = Field()
    meeting = Field()
    download_url = Field()
