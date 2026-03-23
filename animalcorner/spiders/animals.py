import scrapy
from animalcorner.items import AnimalcornerItem

class AnimalsSpider(scrapy.Spider):
    name = "animals"
    allowed_domains = ["animalcorner.org"]
    start_urls = ["https://animalcorner.org/animals"]

    @staticmethod
    def build_description(buffer):
        if not buffer:
            return None

        has_list_content = any(isinstance(entry, list) for entry in buffer)
        if has_list_content:
            description = []
            for entry in buffer:
                if isinstance(entry, list):
                    description.extend(entry)
                else:
                    description.append(entry)
            return description

        return " ".join(buffer)

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

        content_selector = (
            "div.entry-content p, "
            "div.entry-content h2, "
            "div.entry-content h3, "
            "div.entry-content h4, "
            "div.entry-content ul, "
            "div.entry-content ol"
        )

        for element in response.css(content_selector):
            tag = element.root.tag
            text = element.xpath("normalize-space(string())").get()

            if tag in ["h2", "h3", "h4"]:
                # finalize previous heading
                if current_heading and current_description_buffer:
                    facts.append({
                        "title": current_heading,
                        "description": self.build_description(current_description_buffer)
                    })

                current_heading = text
                current_description_buffer = []

            elif tag == "p":
                if text:
                    if current_heading:
                        current_description_buffer.append(text)
                    else:
                        introduction_buffer.append(text)

            elif tag in ["ul", "ol"]:
                list_items = [
                    li.xpath("normalize-space(string())").get()
                    for li in element.css("li")
                ]
                list_items = [item for item in list_items if item]

                if list_items:
                    if current_heading:
                        current_description_buffer.append(list_items)
                    else:
                        introduction_buffer.append(list_items)

        # finalize last heading
        if current_heading and current_description_buffer:
            facts.append({
                "title": current_heading,
                "description": self.build_description(current_description_buffer)
            })

        item["introduction"] = {
            "p": self.build_description(introduction_buffer)
        }

        item["facts"] = facts

        yield item
