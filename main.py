import sys
import os

from scrapy.cmdline import execute


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# execute(["scrapy", "crawl", "tokens"])

# execute(["scrapy", "crawl", "tokenholder"])

# execute(["scrapy", "crawl", "BTCtokenTopHolder"])


# execute(["scrapy", "crawl", "NeblTopHolder"])


# execute(["scrapy", "crawl", "EthSysTopHolder"])

# execute(["scrapy", "crawl", "EthTopHolder"])


execute(["scrapy", "crawl", "CoinMarketCapHistory"])

