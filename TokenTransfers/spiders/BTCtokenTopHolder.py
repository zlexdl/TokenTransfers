# -*- coding: utf-8 -*-
from datetime import datetime
from redis import StrictRedis
import scrapy
from scrapy.loader import ItemLoader

from TokenTransfers.commons import get_holder_name
from TokenTransfers.items import TokenTopHistoryItem


class BtctokentopholderSpider(scrapy.Spider):
    name = 'BTCtokenTopHolder'
    allowed_domains = ['btc.com']
    start_urls = ['http://btc.com/stats/rich-list/',
                  'https://bch.btc.com/stats/rich-list']
    redis = StrictRedis(host='192.168.1.8', port=6379, db=0)

    def parse(self, response):
        tokenTopHistoryItem = TokenTopHistoryItem()
        symbol = 'btc'
        url = response.url
        if url.find('bch') > -1:
            symbol = 'bch'

        # tds = response.css("table.table")
        # for td in tds:
        #     item_loader = ItemLoader(item=TokenTopHistoryItem(), selector=td, response=response)
        #     item_loader.add_css('rank', "tr > td:nth-child(1)::text")
        #     item_loader.add_css('address', "tr > td:nth-child(2) > span > a::text")
        #     item_loader.add_css('quantity', "tr > td:nth-child(3)::text")
        #     item_loader.add_css('transaction', "tr > td:nth-child(5) > span::text")
        #     item_loader.add_css('last_transaction', "tr > td:nth-child(6) > span::text")
        #     # item_loader.add_value('percentage', )
        #
        # tokenTopHistoryItem = item_loader.load_item()
        #
        # yield tokenTopHistoryItem

        rank_tags = response.css("table.table tr > td:nth-child(1)::text").extract()
        address_tags = response.css("table.table tr > td:nth-child(2) > span > a::text").extract()
        quantity_tags = response.css("table.table tr > td:nth-child(3)::text").extract()
        transactions_tags = response.css("table.table tr > td:nth-child(5) > span::text").extract()
        last_transaction_tags = response.css("table.table tr > td:nth-child(6) > span::text").extract()

        for index in range(0, len(rank_tags)):
            rank = rank_tags[index]
            address = address_tags[index].replace('\n', '').strip()
            quantity = float(quantity_tags[index * 2].replace(',', ''))
            transaction = transactions_tags[index].replace('\n', '').strip()
            last_transaction = last_transaction_tags[index].replace('\n', '').strip()
            percentage = round((quantity / 21000000) * 100, 2)

            tokenTopHistoryItem['symbol'] = symbol
            tokenTopHistoryItem['rank'] = rank
            tokenTopHistoryItem['address'] = address
            tokenTopHistoryItem['quantity'] = quantity
            tokenTopHistoryItem['transaction'] = transaction
            tokenTopHistoryItem['last_transaction'] = last_transaction
            tokenTopHistoryItem['percentage'] = percentage
            tokenTopHistoryItem['timestamp'] = datetime.now()
            name = get_holder_name(self, address, symbol)
            tokenTopHistoryItem['name'] = name
            yield tokenTopHistoryItem
        pass
