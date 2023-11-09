from scrapy.crawler import CrawlerProcess
from sInvestSpider import sInvestSpyder
from data_config import DataConfiguration

cprocess = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
})

for ticker in DataConfiguration.TickerList:
    cprocess.crawl(sInvestSpyder, ticker, DataConfiguration.URL)

cprocess.start()