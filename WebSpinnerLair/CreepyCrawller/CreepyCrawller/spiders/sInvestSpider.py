import logging
logging.basicConfig(filename='spider_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from DataConfiguration import DataConfiguration
import scrapy
import csv
import time 

class sInvestSpyder(scrapy.Spider):
    name = 'sInvest'

    def __init__(self, ticker=None, endpoint=None, *args, **kwargs):
        super(sInvestSpyder, self).__init__(*args, **kwargs)
        self.dt = DataConfiguration()
        self.ticker = ticker or 'ENAT3'
        self.url = endpoint or 'https://statusinvest.com.br/acoes/'
        self.csv_file = 'all_tickers_data.csv'
        self.log_file = 'spider_log.log'
        self.tagList = self.dt.tagDictionary

        # Configure logging
        logging.info(f"File Start")
        # Write the header row if the file doesn't exist
        try:
            with open(self.csv_file, 'x', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(['Ticker', 'Company Name', 'Current Value', 'VPA', 'LPA', 'DY', 'ADV'])
        except FileExistsError:
            pass

    def start_requests(self):
        try:
            self.start_urls = [self.url + self.ticker]
            logging.error(f"Request Start to: {self.start_urls}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
            }
            for url in self.start_urls:
                yield scrapy.Request(url, headers=headers, callback=self.parse)
                #time.sleep(2)
        except Exception as e:
            logging.error(f"An error occurred during start_requests: {e}")

    def parse(self, response):
        try:
            # Log HTTP status code
            logging.info(f"Received {response.status} status code for {response.url}")

            # Check if the response status code is 200 (OK)
            if response.status == 200:
                ticker = response.css(self.tagList['Ticker']).get().split(' - ')[0]
                logging.info(f'Ticker: {ticker}')

                cName = response.css(self.tagList['cName']).get()
                logging.info(f'Nome Compania: {cName}')

                valor_atual = response.css(self.tagList['cValue']).get()
                logging.info(f'Valor atual: {valor_atual}')

                vpa = response.css(self.tagList['VPA']).get()
                logging.info(f'VPA: {vpa}')

                lpa = response.css(self.tagList['LPA']).get()
                logging.info(f'LPA: {lpa}')

                DY = response.css(self.tagList['DY']).get()
                logging.info(f'DY: {DY}')

                DV = response.css(self.tagList['DV']).get()
                logging.info(f'DV: {DV}')

                # Append data to the CSV file
                with open(self.csv_file, mode='a', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow([ticker, cName, valor_atual, vpa, lpa, DY, DV])

                logging.info(f'Data appended to {self.csv_file}')

            else:
                # Log other status codes (not 200)
                logging.warning(f"Received {response.status} status code for {response.url}")

        except Exception as e:
            # Log the exception
            logging.error(f"An error occurred while parsing: {e}")
