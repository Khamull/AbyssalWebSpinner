import scrapy
import re

class FullHTML(scrapy.Spider):
    name = 'fullHTML'
    start_urls = ['https://statusinvest.com.br/acoes/enat3']

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        ticker = response.css('h1[title]::text').get().split(' - ')[0]
        print(f'Ticker: {ticker}')
        cName = response.css('h1 small::text').get()
        print(f'Nome Compania: {cName}')
        valor_atual = response.css('div[title="Valor atual do ativo"] strong.value::text').get()
        print(f'Valor atual: {valor_atual}')
        vpa = response.css('div[title="Indica qual o valor patrimonial de uma ação."] strong.value::text').get()
        print(f'VPA: {vpa}')
        lpa = response.css('div[title*="Indicar se a empresa é ou não lucrativa"] strong.value::text').get()
        print(f'LPA: {lpa}')
        # Save the entire HTML response
        filename = 'full_html.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved full HTML to {filename}')