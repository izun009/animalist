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

class AnimalcornerFactsItem(scrapy.Item):
    heading = scrapy.Field()
    description = scrapy.Field()

# class AnimalcornerItem(scrapy.Item):
#     name = scrapy.Field()
#     facts = scrapy.Field()
#     introduction = scrapy.Field()
#     #image_urls = scrapy.Field()

# class H2Item(scrapy.Item):
#     h2 = scrapy.Field()
#     description_h2 = scrapy.Field()
#     subheadings = scrapy.Field()

# class H3Item(scrapy.Item):
#     h3 = scrapy.Field()
#     description_h3 = scrapy.Field()

# class AnimalcornerFactsItem(scrapy.Item):
#     fact = scrapy.Field()
#     description = scrapy.Field()