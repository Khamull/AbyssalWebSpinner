import scrapy

class SpySpider(scrapy.Spider):
    name = 'api_spider'
    start_urls = ['https://arquivos.b3.com.br/tabelas/InstrumentsConsolidated/2023-11-03?lang=pt']

    def parse(self, response):
        # Extract all links from the page
        links = response.xpath('//a/@href').extract()

        # Iterate through the links
        for link in links:
            # Join the link with the base URL to get the full endpoint URL
            endpoint_url = response.urljoin(link)

            # Make a request to the endpoint URL
            yield scrapy.Request(
                url=endpoint_url,
                callback=self.parse_endpoint
            )

    def parse_endpoint(self, response):
        # Check if the response status code is not 404
        if response.status != 404:
            yield {
                'endpoint': response.url,
                'status_code': response.status
            }
    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)