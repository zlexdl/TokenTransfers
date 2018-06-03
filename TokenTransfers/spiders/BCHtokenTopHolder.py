# -*- coding: utf-8 -*-
from datetime import datetime
# from redis import StrictRedis
import scrapy
from TokenTransfers.commons import get_holder_name_mongodb
from TokenTransfers.items import TokenTopHistoryItem
from pymongo import MongoClient


class BtctokentopholderSpider(scrapy.Spider):
    name = 'BCHtokenTopHolder'
    allowed_domains = ['btc.com']
    start_urls = ['https://bch.btc.com/stats/rich-list']
    # redis = StrictRedis(host='192.168.1.8', port=6379, db=0)
    symbol = 'bch'
    conn = MongoClient('192.168.1.8', 27017)
    db = conn.explorerdb_bch
    token_address = db.holders
    rich_count = 100

    def parse(self, response):
        tokenTopHistoryItem = TokenTopHistoryItem()
        rank_tags = response.css("table.table tr > td:nth-child(1)::text").extract()
        address_tags = response.css("table.table tr > td:nth-child(2) > span > a::attr(href)").extract()
        quantity_tags = response.css("table.table tr > td:nth-child(3)::text").extract()
        transactions_tags = response.css("table.table tr > td:nth-child(5) > span::text").extract()
        last_transaction_tags = response.css("table.table tr > td:nth-child(6) > span::text").extract()

        for index in range(0, len(rank_tags)):
            rank = rank_tags[index]
            address = address_tags[index].replace('https://bch.btc.com/', '').strip()
            quantity = float(quantity_tags[index * 2].replace(',', ''))
            transaction = transactions_tags[index].replace('\n', '').strip()
            last_transaction = last_transaction_tags[index].replace('\n', '').strip()
            percentage = round((quantity / 21000000) * 100, 2)

            tokenTopHistoryItem['symbol'] = self.symbol
            tokenTopHistoryItem['rank'] = rank
            tokenTopHistoryItem['address'] = address
            tokenTopHistoryItem['quantity'] = quantity
            tokenTopHistoryItem['transaction'] = transaction
            tokenTopHistoryItem['last_transaction'] = last_transaction
            tokenTopHistoryItem['percentage'] = percentage
            tokenTopHistoryItem['timestamp'] = datetime.now()
            name = get_holder_name_mongodb(self, address, rank)
            tokenTopHistoryItem['name'] = name
            yield tokenTopHistoryItem
        pass
