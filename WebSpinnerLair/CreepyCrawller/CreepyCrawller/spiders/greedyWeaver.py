# comand to run locally scrapy runspider CreepyCrawller/CreepyCrawller/spiders/greedyWeaver.py -o tickers.json
# it saves the quotes to the json file quotes.json

import scrapy
from bs4 import BeautifulSoup

class GreedySpider(scrapy.Spider):
    name = 'GreedySpider'
    start_urls = ['https://statusinvest.com.br/acoes/enat3']

    def parse(self, response):
        with open('full_html.html', 'wb') as f:
            f.write(response.body)
        # Parse the entire HTML response
        html_content = response.body
        # Extract data from the table rows
        
        # Create a BeautifulSoup object for parsing
        soup = BeautifulSoup(html_content, 'html.parser')

