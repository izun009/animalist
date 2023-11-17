import scrapy
from animalcorner.items import AnimalcornerItem, AnimalcornerFactsItem

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
        item['name'] = response.css('header.entry-header h1.entry-title::text').get()
        item['introduction'] = []
        item['facts'] = []

        current_heading = None
        current_h2 = None
        current_h3 = None
        current_h4 = None

        for element in response.css('div.entry-content p, div.entry-content h2, div.entry-content h3, div.entry-content h4'):
            tag = element.root.tag
            text = element.get()

            if tag in ['h2', 'h3', 'h4']:
                # Append the previous data and reset subheadings
                if current_heading:
                    if current_heading['tag'] == 'h2':
                        item['facts'].append(current_heading)
                    elif current_heading['tag'] == 'h3':
                        item['facts'].append(current_heading)
                    elif current_heading['tag'] == 'h4':
                        item['facts'].append(current_heading)

                current_heading = {'tag': tag, 'text': text, 'description': []}
            elif tag == 'p':
                if current_heading:
                    current_heading['description'].append({'p': text})
                else:
                    item['introduction'].append({'p': text})

        # Append the last heading data
        if current_heading:
            if current_heading['tag'] == 'h2':
                item['facts'].append(current_heading)
            elif current_heading['tag'] == 'h3':
                item['facts'].append(current_heading)
            elif current_heading['tag'] == 'h4':
                item['facts'].append(current_heading)

        yield item


    # def parse_animals(self, response):
    #     item = AnimalcornerItem()
    #     item['name'] = response.css('header.entry-header h1.entry-title::text').get()
    #     # item['introduction'] = response.css('div.entry-content p, p:has(strong)').xpath('normalize-space(string())').getall()

    #     facts_list = []
    #     h2_facts = response.css('h2.wp-block-heading')
    #     for h2 in h2_facts:
    #         fact = AnimalcornerFactsItem()
    #         fact['fact'] = h2.css('::text').get()

    #         # descriptions = []
    #         # # Iterate over following-sibling p elements and extract descriptions
    #         # for p in h2.xpath('following-sibling::p'):
    #         #     description = p.xpath('normalize-space(string())').get()
    #         #     descriptions.append(description)
    #         # # Add descriptions list to the fact item
    #         # fact['description'] = descriptions
    #         # facts_list.append(dict(fact))

    #         fact['description'] = h2.xpath('following-sibling::p[1]').xpath('normalize-space(string())').get()
    #         facts_list.append(dict(fact))
            
    #     # add the facts list to the item
    #     item['facts'] = facts_list
    #     yield item
    

    # scrape name, facts, image_urls, and endpoint
    # def parse_animals(self, response):
    #     item = AnimalcornerItem()
    #     item['name'] = response.css('header.entry-header h1.entry-title::text').get()

    #     for entry_content in response.css('article.animals'):
    #         all_data = []

    #         # Check if there is a heading immediately following the entry-content
    #         has_heading_after_entry_content = entry_content.css('div.entry-content h2, div.entry-content h3')

    #         introductory_paragraphs = entry_content.xpath('div[@class="entry-content"]/p')

    #         if not has_heading_after_entry_content:
    #             # If no heading follows entry-content, scrape introductory <p> tags
    #             for paragraph in introductory_paragraphs:
    #                 text = paragraph.get()
    #                 all_data.append({"p": text})
    #         else:
    #             introductory_paragraphs = None  # Set introduction to None when there is a heading

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
    #         item["introduction"] = all_data if not has_heading_after_entry_content else None
    #         item["facts"] = all_data if has_heading_after_entry_content else []
    #     yield item


    # def parse_animals(self, response):
    #     item = AnimalcornerItem()
    #     item['name'] = response.css('header.entry-header h1.entry-title::text').get()
    #     item['facts'] = []

    #     current_h2 = None
    #     current_h3 = None
    #     current_h4 = None
    #     current_h5 = None
    #     current_h6 = None

    #     for element in response.css('div.entry-content h2, div.entry-content h3, div.entry-content h4, div.entry-content h5, div.entry-content h6, div.entry-content p'):
    #         tag = element.root.tag
    #         text = element.get()

    #         if tag == 'h2':
    #             # Append the previous h2 data and reset subheadings
    #             if current_h2:
    #                 item['facts'].append(current_h2)
    #             current_h2 = {"h2": text, "description": []}
    #             current_h3 = None
    #         elif tag == 'h3':
    #             # Append the previous h3 data
    #             if current_h3:
    #                 current_h2["description"].append(current_h3)
    #             current_h3 = {"h3": text, "description": []}
    #             current_h4 = None
    #         elif tag == 'h4':
    #             # Append the previous h4 data
    #             if current_h4:
    #                 current_h3["description"].append(current_h4)
    #             current_h4 = {"h4": text, "description": []}
    #             current_h5 = None
    #         elif tag == 'h5':
    #             # Append the previous h5 data
    #             if current_h5:
    #                 current_h4["description"].append(current_h5)
    #             current_h5 = {"h5": text, "description": []}
    #             current_h6 = None
    #         elif tag == 'h6':
    #             # Append the previous h6 data
    #             if current_h6:
    #                 current_h5["description"].append(current_h6)
    #             current_h6 = {"h6": text, "description": []}
    #         elif tag == 'p':
    #             # Check the current heading level and append to the description
    #             if current_h6:
    #                 current_h6["description"].append({"p": text})
    #             elif current_h5:
    #                 current_h5["description"].append({"p": text})
    #             elif current_h4:
    #                 current_h4["description"].append({"p": text})
    #             elif current_h3:
    #                 current_h3["description"].append({"p": text})
    #             elif current_h2:
    #                 current_h2["description"].append({"p": text})

    #     # Append the last h2 data
    #     if current_h2:
    #         item['facts'].append(current_h2)

    #     return item

    # OK
    # def parse_animals(self, response):
    #     item = AnimalcornerItem()
    #     item['name'] = response.css('article.animals header.entry-header h1.entry-title::text').get()

    #     introductory_paragraphs = response.css('article.animals header.entry-header + div.entry-content > p')

    #     if introductory_paragraphs:
    #         item['introduction'] = [{'p': paragraph.get()} for paragraph in introductory_paragraphs]

    #         # Check if there is an h2 after the last p of the introduction
    #         h2_after_intro = response.css('article.animals div.entry-content > p:last-child + h2::text').get()

    #         if h2_after_intro:
    #             # Stop scraping introduction and start scraping h2 as facts
    #             item['facts'] = [{"h2": h2_after_intro, "description": []}]
    #             return item

    #     item['facts'] = []

    #     current_h2 = None
    #     current_h3 = None

    #     for element in response.css('article.animals div.entry-content h2, article.animals div.entry-content h3, article.animals div.entry-content p'):
    #         tag = element.root.tag
    #         text = element.get()

    #         if tag == 'h2':
    #             # Append the previous h2 data and reset subheadings
    #             if current_h2:
    #                 item['facts'].append(current_h2)
    #             current_h2 = {"h2": text, "description": []}
    #             current_h3 = None
    #         elif tag == 'h3':
    #             # Append the previous h3 data
    #             if current_h3:
    #                 current_h2["description"].append(current_h3)
    #             current_h3 = {"h3": text, "description": []}
    #         elif tag == 'p':
    #             # Check the current heading level and append to the description
    #             if current_h3:
    #                 current_h3["description"].append({"p": text})
    #             elif current_h2:
    #                 current_h2["description"].append({"p": text})

    #     # Append the last h2 data
    #     if current_h2:
    #         item['facts'].append(current_h2)

    #     yield item
