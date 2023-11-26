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
        item['introduction'] = []
        item['facts'] = []

        current_h2 = None
        current_h3 = None
        current_h4 = None

        for element in response.css('div.entry-content p, div.entry-content h2, div.entry-content h3, div.entry-content h4'):
            heading = element.root.tag
            text = element.get()

            if heading == 'h2':
                # Append the previous h2 data and reset subheadings
                if current_h2:
                    item['facts'].append(current_h2)
                current_h2 = {"h2": text, "description_h2": []}
                current_h3 = None
                current_h4 = None
            elif heading == 'h3':
                # Append the previous h3 data
                if current_h3:
                    item['facts'].append(current_h3)
                current_h3 = {"h3": text, "description_h3": []}
                current_h4 = None
            elif heading == 'h4':
                if current_h4:
                    item['facts'].append(current_h4)
                current_h4 = {"h4": text, "description_h4": []}
            elif heading == 'p':
                if current_h2:
                    current_h2["description_h2"].append(text)
                elif current_h3:
                    current_h3["description_h3"].append(text)
                elif current_h4:
                    current_h4["description_h4"].append(text)
                else:
                    item["introduction"].append({'p': text})

        # Append the last h2 data
        if current_h2:
            item['facts'].append(current_h2)
        elif current_h3:
            item['facts'].append(current_h3)
        elif current_h4:
            item['facts'].append(current_h4)

        yield item
