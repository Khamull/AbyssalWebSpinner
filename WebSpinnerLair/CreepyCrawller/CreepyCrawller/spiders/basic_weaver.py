# comand to run locally scrapy runspider CreepyCrawller/CreepyCrawller/spiders/basic_weaver.py -o quotes.json
# it saves the quotes to the json file quotes.json

import scrapy

class BasicSpider(scrapy.Spider):
    name = 'basic'
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)