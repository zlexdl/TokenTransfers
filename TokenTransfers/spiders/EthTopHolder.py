# -*- coding: utf-8 -*-
import re

import scrapy
from datetime import datetime
# from redis import StrictRedis
from TokenTransfers.commons import get_holder_name_mongodb
from TokenTransfers.items import TokenTopHistoryItem
from scrapy.http import Request
from pymongo import MongoClient


class EthtopholderSpider(scrapy.Spider):
    name = 'EthTopHolder'
    allowed_domains = ['etherscan.io']
    start_urls = ['https://etherscan.io/accounts/']
    # redis = StrictRedis(host='192.168.1.8', port=6379, db=0)
    conn = MongoClient('192.168.1.8', 27017)
    db = conn.token_address
    token_address = db.eth
    rich_count = 100
    symbol = 'eth'

    def parse(self, response):
        tokenTopHistoryItem = TokenTopHistoryItem()
        rank_tags = response.css("table.table tr > td:nth-child(1)::text").extract()
        quantity_tags = response.css("table.table tr > td:nth-child(3)").extract()

        address_tgas = response.css("table.table tr > td:nth-child(2)>a::text").extract()
        percentage_tags = response.css("table.table tr > td:nth-child(4)::text").extract()

        for index in range(0, len(rank_tags)):
            rank = rank_tags[index]
            match_re = re.match('^<td>([\d,]+)<b>.+', quantity_tags[index])
            if match_re:
                quantity = float(match_re.group(1).replace(',', ''))
            else:
                quantity = float(quantity_tags[index].replace(',', '').replace(' Ether', '').replace('<td>', '').replace('</td>', ''))

            address = address_tgas[index]
            percentage = round(float(percentage_tags[index].replace('%', '')), 3)

            tokenTopHistoryItem['symbol'] = self.symbol
            tokenTopHistoryItem['rank'] = rank
            tokenTopHistoryItem['address'] = address
            tokenTopHistoryItem['quantity'] = quantity
            tokenTopHistoryItem['percentage'] = percentage
            tokenTopHistoryItem['timestamp'] = datetime.now()
            name = get_holder_name_mongodb(self, address, rank)
            tokenTopHistoryItem['name'] = name
            yield tokenTopHistoryItem

        for index in range(2, 5):
            yield Request(url="https://etherscan.io/accounts/" + str(index),
                          callback=self.parse)
