# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class AnimalcornerItem(scrapy.Item):
    name = scrapy.Field()
    fact = scrapy.Field()
    #image_urls = scrapy.Field()
