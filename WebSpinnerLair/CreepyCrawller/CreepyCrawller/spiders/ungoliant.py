from multiprocessing import Process
from scrapy.crawler import CrawlerProcess
from .stockspider import stockSpider
from .DataConfiguration import DataConfiguration
from fake_useragent import UserAgent
import time
import random
def run_spider(spider_class, tickers, url):
    ua = UserAgent()
    process = CrawlerProcess({
        'User-Agent': ua.random
    })

    for ticker in tickers:
        process.crawl(spider_class, ticker, url)

    process.start()
    process.join()  # Wait for the process to finish

def main():

    dt = DataConfiguration()
    dt.leCSV()
    batch_size = 5

    for start_index in range(0, len(dt.TickerList), batch_size):

        end_index = min(start_index + batch_size, len(dt.TickerList))
        tickers_batch = dt.TickerList[start_index:end_index]
        process = Process(target=run_spider, args=(stockSpider, tickers_batch, dt.URL))
        process.start()
        process.join()  # Wait for the process to finish
        random_number = random.randint(1, 10)
        time.sleep(random_number)

if __name__ == "__main__":
    main()
