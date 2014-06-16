# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TaipeiItem(Item):
    sitting = Field()
    category = Field()
    date = Field()
    meeting = Field()
    download_url = Field()
