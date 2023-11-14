from multiprocessing import Process
from scrapy.crawler import CrawlerProcess
from sInvestSpider import sInvestSpyder
from DataConfiguration import DataConfiguration

def run_spiders(tickers, url):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    })

    for ticker in tickers:
        process.crawl(sInvestSpyder, ticker, url)

    process.start()
    process.join()  # Wait for the process to finish

def main():
    dt = DataConfiguration()
    dt.leCSV()

    batch_size = 5

    for start_index in range(0, len(dt.TickerList), batch_size):
        end_index = min(start_index + batch_size, len(dt.TickerList))
        tickers_batch = dt.TickerList[start_index:end_index]

        process = Process(target=run_spiders, args=(tickers_batch, dt.URL))
        process.start()
        process.join()  # Wait for the process to finish

if __name__ == "__main__":
    main()
