# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class WebScrappingSpiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = Field()
    title = Field()
    content = Field()
    last_modified = Field()
    pass
