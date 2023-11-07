import scrapy
from animalcorner.items import AnimalcornerItem

class AnimalsSpider(scrapy.Spider):
    name = "animals"
    allowed_domains = ["animalcorner.org"]
    start_urls = ["https://animalcorner.org/animals"]

    def parse(self, response):
        animals_link = response.css("div.one-third a::attr(href)")
        for anim in animals_link:
            yield response.follow(anim, self.parse_animals)

    def parse_animals(self, response):
        item = AnimalcornerItem()

        item['name'] = response.css("h1.entry-title::text").get()
        animal_name = item['name']
        header_facts = response.css('div.entry-content h2.wp-block-heading::text, div.entry-content h3.wp-block-heading::text, div.entry-content h4.wp-block-heading::text, div.entry-content h5.wp-block-heading::text, div.entry-content h6.wp-block-heading::text')
        if not header_facts:
            item['fact'] = "fact about "+animal_name

        for header in header_facts:
            #item = AnimalcornerItem()
            header_text = header.get()
            item['fact'] = header_text
        #item['fact'] = response.css("h3.wp-block-heading::text").get()

        yield item
