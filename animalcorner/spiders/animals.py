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
    #     item['name'] = response.css('h1.entry-title::text').get()

    #     for entry_content in response.css('div.entry-content'):
    #         all_data = []

    #         # Check if there is a heading immediately following the title
    #         first_heading = entry_content.xpath('h1/following-sibling::h2[1] | h1/following-sibling::h3[1]')

    #         if first_heading:
    #             # Scrape the first heading after the title
    #             introductory_paragraphs = entry_content.xpath('h1/following-sibling::h2[1]/preceding-sibling::p | h1/following-sibling::h3[1]/preceding-sibling::p')
    #         else:
    #             # Scrape the introductory <p> tags if there is no heading
    #             introductory_paragraphs = entry_content.xpath('h1/following-sibling::p')

    #         for paragraph in introductory_paragraphs:
    #             text = paragraph.get()
    #             all_data.append({"p": text})

    #         # Reset current_h2 and current_h3
    #         current_h2 = None
    #         current_h3 = None

    #         for element in entry_content.css('h2, h3, p'):
    #             tag = element.root.tag
    #             text = element.get()

    #             if tag == 'h2':
    #                 # Append the previous h2 data and reset subheadings
    #                 if current_h2:
    #                     all_data.append(current_h2)
    #                 current_h2 = {"h2": text, "description_h2": [], "subheadings": []}
    #                 current_h3 = None
    #             elif tag == 'h3':
    #                 # Append the previous h3 data
    #                 if current_h3:
    #                     current_h2["subheadings"].append(current_h3)
    #                 current_h3 = {"h3": text, "description_h3": []}
    #             elif tag == 'p':
    #                 if current_h3:
    #                     current_h3["description_h3"].append(text)
    #                 elif current_h2:
    #                     current_h2["description_h2"].append(text)

    #         # Append the last h2 data
    #         if current_h2:
    #             all_data.append(current_h2)

    #         item["facts"] = all_data

    #     yield item



    def parse_animals(self, response):
        item = AnimalcornerItem()
        item['name'] = response.css('h1.entry-title::text').get()
        facts = []

        for entry_content in response.css('div.entry-content'):
            all_data = []

            # Check if there is a heading immediately following the title
            first_heading = entry_content.xpath('h1/following-sibling::h2[1] | h1/following-sibling::h3[1]')

            if first_heading:
                # Scrape the first heading after the title
                first_heading = first_heading[0].get()
                all_data.append({"h2": first_heading})

            # Scrape introductory <p> tags after the name of the animal
            introductory_data = entry_content.xpath('h1/following-sibling::p | h1/following-sibling::text()[not(following-sibling::h2 | following-sibling::h3)]')

            for data in introductory_data:
                text = data.get()
                all_data.append({"description_h2": [text]})

            # Reset current_h2 and current_h3
            current_h2 = None
            current_h3 = None

            for element in entry_content.css('h2, h3, p'):
                tag = element.root.tag
                text = element.get()

                if tag == 'h2':
                    # Append the previous h2 data and reset subheadings
                    if current_h2:
                        all_data.append(current_h2)
                    current_h2 = {"h2": text, "description_h2": [], "subheadings": []}
                    current_h3 = None
                elif tag == 'h3':
                    # Append the previous h3 data
                    if current_h3:
                        current_h2["subheadings"].append(current_h3)
                    current_h3 = {"h3": text, "description_h3": []}
                elif tag == 'p':
                    if current_h3:
                        current_h3["description_h3"].append(text)
                    elif current_h2:
                        current_h2["description_h2"].append(text)

            # Append the last h2 data
            if current_h2:
                all_data.append(current_h2)

            # Check if there are any facts scraped
            if all_data:
                facts.extend(all_data)

        item["facts"] = facts
        yield item

       