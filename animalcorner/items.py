# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# items.py
import scrapy

class AnimalcornerItem(scrapy.Item):
    name = scrapy.Field()
    introduction = scrapy.Field()
    facts = scrapy.Field()
    description = scrapy.Field()
    images = scrapy.Field()
