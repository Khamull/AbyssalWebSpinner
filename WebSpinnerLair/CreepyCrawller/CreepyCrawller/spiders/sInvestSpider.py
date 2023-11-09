#url = https://statusinvest.com.br/acoes/
#ticker enat3
#taglist.tagDictionary['Ticker']
from data_config import DataConfiguration
import scrapy
import csv

class sInvestSpyder(scrapy.Spider):
    
    name = 'sInvest'
    
    def __init__(self, ticker=None, endpoint=None, *args, **kwargs):
        super(sInvestSpyder, self).__init__(*args, **kwargs)
        self.ticker = ticker or 'ENAT3'
        self.url = endpoint or 'https://statusinvest.com.br/acoes/'
        self.tagList = DataConfiguration()
        print(self.url)
        print(self.ticker)
        
        
    def start_requests(self):
        print('start request ' + self.url)
        print('start request ' + self.ticker)
        self.start_urls = [self.url + self.ticker]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        
        ticker = response.css(self.tagList.tagDictionary['Ticker']).get().split(' - ')[0]
        print(f'Ticker: {ticker}')
        cName = response.css(self.tagList.tagDictionary['cName']).get()
        print(f'Nome Compania: {cName}')
        valor_atual = response.css(self.tagList.tagDictionary['cValue']).get()
        print(f'Valor atual: {valor_atual}')
        vpa = response.css(self.tagList.tagDictionary['VPA']).get()
        print(f'VPA: {vpa}')
        lpa = response.css(self.tagList.tagDictionary['LPA']).get()
        print(f'LPA: {lpa}')
        DY = response.css(self.tagList.tagDictionary['DY']).get()
        print(f'DY: {DY}')

        # Define the CSV file name
        csv_file = f'{ticker}_data.csv'

        # Write the data to the CSV file
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Ticker', 'Company Name', 'Current Value', 'VPA', 'LPA', 'Dividend Yield'])
            writer.writerow([ticker, cName, valor_atual, vpa, lpa, DY])

        print(f'Data written to {csv_file}')
