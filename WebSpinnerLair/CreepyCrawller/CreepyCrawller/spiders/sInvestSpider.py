#url = https://statusinvest.com.br/acoes/
#https://statusinvest.com.br/acao/payoutresult?code=csna3&companyid=397&type=2
#https://statusinvest.com.br/acao/payoutresult?code=csna3
#ticker enat3
#taglist.tagDictionary['Ticker']
from data_config import DataConfiguration
import scrapy
import csv
import json

class sInvestSpyder(scrapy.Spider):
    
    name = 'sInvest'
    # download_delay = 5  # Add this line to introduce a 1-second delay
    # custom_settings = {
    #     'CONCURRENT_REQUESTS': 5,
    # }
    
    def __init__(self, ticker=None, endpoint=None, *args, **kwargs):
        super(sInvestSpyder, self).__init__(*args, **kwargs)
        self.ticker = ticker or 'ENAT3'
        self.url = endpoint or 'https://statusinvest.com.br/acoes/'
        self.csv_file = 'all_tickers_data.csv'
        self.tagList = DataConfiguration()
        # Write the header row if the file doesn't exist
        try:
            with open(self.csv_file, 'x', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(['Ticker', 'Company Name', 'Current Value', 'VPA', 'LPA', 'DY', 'ADV'])
        except FileExistsError:
            pass
        print(self.url)
        print(self.ticker)

    # def parse_payout(self, response):
    #     ticker = response.meta['ticker']
    #     json_data = json.loads(response.text)
    #     avg_value = json_data['avg']

    #     # Now you can use the 'avg_value' as needed, for example, print it
    #     print(f'Average Value for {ticker}: {avg_value}')
        
        
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
        DV = response.css(self.tagList.tagDictionary['DV']).get()
        print(f'DV: {DV}')
        
        # After processing the initial response, make a second request to the payout URL
        # payout_url = f'https://statusinvest.com.br/acao/payoutresult?code={ticker}'
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        # }
        # yield scrapy.Request(payout_url, callback=self.parse_payout, meta={'ticker': ticker})
        # PO = avg_value
         # Append data to the CSV file
        with open(self.csv_file, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([ticker, cName, valor_atual, vpa, lpa, DY, DV])

        print(f'Data appended to {self.csv_file}')