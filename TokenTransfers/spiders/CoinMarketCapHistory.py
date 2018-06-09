# -*- coding: utf-8 -*-
from datetime import datetime
import json

import scrapy

from TokenTransfers.items import coinmarketcapItem


class CoinmarketcaphistorySpider(scrapy.Spider):
    name = 'CoinMarketCapHistory'
    allowed_domains = ['api.coinmarketcap.com/v1/ticker']
    start_urls = []

    def __init__(self):
        self.start_urls.append('https://api.coinmarketcap.com/v1/ticker/')
        for i in range(2, 16):
            i100 = i * 100 + 1
            self.start_urls.append("https://api.coinmarketcap.com/v1/ticker/?start=" + str(i100))

    def parse(self, response):
        main_data = json.loads(response.body.decode("utf-8"))
        item = coinmarketcapItem()

        for index in range(len(main_data)):
            data = main_data[index]

            item['id'] = data['id']
            item['name'] = data['name']
            item['symbol'] = data['symbol']
            item['rank'] = data['rank']
            item['price_usd'] = data['price_usd']
            item['price_btc'] = data['price_btc']
            item['s24h_volume_usd'] = data['24h_volume_usd']
            item['market_cap_usd'] = data['market_cap_usd']
            item['available_supply'] = data['available_supply']
            item['total_supply'] = data['total_supply']
            item['max_supply'] = data['max_supply']
            item['percent_change_1h'] = data['percent_change_1h']
            item['percent_change_24h'] = data['percent_change_24h']
            item['percent_change_7d'] = data['percent_change_7d']
            item['last_updated'] = datetime.fromtimestamp(float(data['last_updated']))
            yield item

