# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Councilor(Item):
    name = Field()
    ad = Field()
    title = Field()
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
    last_action = Field()
    proposed_by = Field()
    committee = Field()
    resolusion_date = Field()
    resolusion_sitting = Field()
    resolusion = Field()
    bill_no = Field()
    intray_date = Field()
    intray_no = Field()
    receipt_date = Field()
    examination_date = Field()
    examination = Field()
    dispatch_no = Field()
    dispatch_date = Field()
    execution = Field()
    remark = Field()
    links = Field()

class MeetingMinutes(Item):
    sitting = Field()
    category = Field()
    date = Field()
    meeting = Field()
    download_url = Field()
