from multiprocessing import Pool
from sInvestSpider import sInvestSpider
from data_config import DataConfiguration

class SpiderRunner:
    def __init__(self):
        self.data_config = DataConfiguration()

    def run_spider(self, ticker, url):
        spider = sInvestSpider(ticker=ticker, endpoint=url)
        spider.start()

    def run(self):
        for ticker in self.data_config.TickerList :
            with Pool() as p:
                p.starmap(self.run_spider, ticker, )
                self.data_config.URL  


# Example usage
runner = SpiderRunner()
runner.run()