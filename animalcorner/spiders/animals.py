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

    # scrape name, facts, image_urls, and endpoint
    def parse_animals(self, response):
        item = AnimalcornerItem()
        item['name'] = response.css('header.entry-header h1.entry-title::text').get()
        item['images'] = response.css('div.featured-image-wrapper img::attr(data-breeze)').getall()
        item['introduction'] = []
        item['facts'] = []

        current_h = None
        current_h_has_description = False

        for element in response.css('div.entry-content p, div.entry-content h2, div.entry-content h3, div.entry-content h4'):
            tag = element.root.tag
            text = element.xpath('normalize-space(string())').get()

            if tag in ['h2', 'h3', 'h4']:
                # Append the previous data and reset subtags
                if current_h and current_h_has_description:
                    item['facts'].append(current_h)
                current_h = {tag: text, "description": []}
                current_h_has_description = False
            elif tag == 'p':
                if current_h:
                    current_h["description"].append(text)
                    current_h_has_description = True
                else:
                    item["introduction"].append({'p': text})

        # Append the last heading data
        if current_h and current_h_has_description:
            item['facts'].append(current_h)

        yield item
