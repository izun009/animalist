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

    # def parse_animals(self, response):
    #     item = AnimalcornerItem()

    #     item['name'] = response.css("h1.entry-title::text").get()
    #     animal_name = item['name']
    #     #header_facts = response.css('div.entry-content h2.wp-block-heading, div.entry-content h3.wp-block-heading, div.entry-content h4.wp-block-heading, div.entry-content h5.wp-block-heading, div.entry-content h6.wp-block-heading::text')
    #     header_facts = response.css('div.entry-content h2, div.entry-content h3, div.entry-content h4, div.entry-content h5, div.entry-content h6')
        
    #     # if not header_facts:
    #     #     item['fact'] = "Fact about "+animal_name

    #     for header in header_facts:
    #         #item = AnimalcornerItem()
    #         header_text = header.css('::text').get()
    #         item['fact'] = header_text
    #     #item['fact'] = response.css("h3.wp-block-heading::text").get()

    #     yield item

    def parse_animals(self, response):
        item = AnimalcornerItem()
        item['name'] = response.css("h1.entry-title::text").get()
        animal_name = item['name']

        for entry_content in response.css('div.entry-content'):

            all_headings = []

            current_h2 = None
            current_h3 = None

            for element in entry_content.css('h2, h3'):
                tag = element.root.tag
                text = element.get()

                if tag == 'h2':
                    # Check if current_h3 is defined and has content
                    if current_h3 and current_h3["text"]:
                        # Append current_h3 to current_h2
                        if "subheadings" not in current_h2:
                            current_h2["subheadings"] = []
                        current_h2["subheadings"].append(current_h3)
                    
                    # Append current_h2 to all_headings
                    if current_h2 and current_h2["text"]:
                        all_headings.append(current_h2)
                    
                    # Initialize current_h2
                    current_h2 = {"text": text, "subheadings": []}
                    current_h3 = None
                elif tag == 'h3':
                    # Check if current_h3 is defined and has content
                    if current_h3 and current_h3["text"]:
                        # Append current_h3 to current_h2
                        if "subheadings" not in current_h2:
                            current_h2["subheadings"] = []
                        current_h2["subheadings"].append(current_h3)
                    
                    # Initialize current_h3
                    current_h3 = {"text": text}

            # Append the last current_h2
            if current_h2 and current_h2["text"]:
                all_headings.append(current_h2)

            item["facts"] = all_headings


        yield item
