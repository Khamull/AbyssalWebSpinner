import logging
from .DataConfiguration import DataConfiguration
from fake_useragent import UserAgent
import scrapy
import pandas as pd
from stockModel import StockData  # Add this import
import os
from CSVHandler import CSVHandler

class stockSpider(scrapy.Spider):
    name = "stockSpider"

    def __init__(self, ticker=None, endpoint=None, *args, **kwargs):
        super(stockSpider, self).__init__(*args, **kwargs)
        self.dt = DataConfiguration()
        self.ticker = ticker or 'ENAT3'
        self.url = endpoint or 'https://statusinvest.com.br/acoes/'
        self.csv_file = self.dt.myGeneratedCsvFile[0]
        self.tagList = self.dt.tagDictionary
        self.csv_handler = CSVHandler(self.csv_file, StockData)
        # Ensure the CSV file exists, and create it with the header row if it doesn't
        self.csv_handler.create_file_with_header()
        
        logging.basicConfig(filename='spider_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        # Start Log
        logging.info(f"File Start")

    def start_requests(self):
        self.start_urls = [self.url + self.ticker]
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)
    
    def extract_data(self, response):

        ticker = response.css(self.tagList['Ticker']).get().split(' - ')[0]
        company_name = response.css(self.tagList['cName']).get()
        current_value = response.css(self.tagList['cValue']).get()
        vpa = response.css(self.tagList['VPA']).get()
        lpa = response.css(self.tagList['LPA']).get()
        dy = response.css(self.tagList['DY']).get()
        dv = response.css(self.tagList['DV']).get()
        pl = response.css(self.tagList['PL']).get()
        pv = response.css(self.tagList['PV']).get()

        logging.info(f'Ticker: {ticker}')
        logging.info(f'Nome Companhia: {company_name}')
        logging.info(f'Valor atual: {current_value}')
        logging.info(f'VPA: {vpa}')
        logging.info(f'LPA: {lpa}')
        logging.info(f'DY: {dy}')
        logging.info(f'DV: {dv}')
        logging.info(f'PL: {pl}')
        logging.info(f'PV: {pv}')

        return StockData(ticker, company_name, current_value, vpa, lpa, dy, dv, pl, pv)

    def parse(self, response):
        try:
            # Log HTTP status code
            logging.info(f"Received {response.status} status code for {response.url}")

            # Check if the response status code is 200 (OK)
            if response.status == 200:
                stock_data = self.extract_data(response)

                # Append data to the CSV file
                self.csv_handler.append_data(stock_data)

                logging.info(f'Data appended to {self.csv_file}')

            else:
                # Log other status codes (not 200)
                logging.warning(f"Received {response.status} status code for {response.url}")

        except Exception as e:
            # Log the exception
            logging.error(f"An error occurred while parsing: {e}")


