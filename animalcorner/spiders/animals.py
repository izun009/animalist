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
        item["name"] = response.css(
            "header.entry-header h1.entry-title::text"
        ).get()
        item["endpoint"] = response.url
        item["images"] = response.css(
            "div.featured-image-wrapper img::attr(data-breeze)"
        ).getall()

        introduction_buffer = []
        facts = []

        current_heading = None
        current_description_buffer = []

        for element in response.css(
            "div.entry-content p, div.entry-content h2, div.entry-content h3, div.entry-content h4"
        ):
            tag = element.root.tag
            text = element.xpath("normalize-space(string())").get()

            if tag in ["h2", "h3", "h4"]:
                # finalize previous heading
                if current_heading and current_description_buffer:
                    facts.append({
                        "title": current_heading,
                        "description": " ".join(current_description_buffer)
                    })

                current_heading = text
                current_description_buffer = []

            elif tag == "p":
                if current_heading:
                    current_description_buffer.append(text)
                else:
                    introduction_buffer.append(text)

        # finalize last heading
        if current_heading and current_description_buffer:
            facts.append({
                "title": current_heading,
                "description": " ".join(current_description_buffer)
            })

        item["introduction"] = {
            "p": " ".join(introduction_buffer)
        }

        item["facts"] = facts

        yield item
