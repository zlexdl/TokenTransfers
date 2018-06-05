# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose

class TokentransfersItem(scrapy.Item):
    symbol = scrapy.Field()
    symbol_address = scrapy.Field()
    token_name = scrapy.Field()
    from_address = scrapy.Field()
    to_address = scrapy.Field()
    num = scrapy.Field()
    in_or_out = scrapy.Field()
    transfer_token = scrapy.Field()
    date = scrapy.Field()
    is_ex_address = scrapy.Field()
    # percent = scrapy.Field()
    # rank = scrapy.Field()


class TokenTopHistoryItem(scrapy.Item):
    symbol = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    quantity = scrapy.Field()
    rank = scrapy.Field()
    percentage = scrapy.Field()
    timestamp = scrapy.Field()
    transaction = scrapy.Field()
    last_transaction = scrapy.Field()


class coinmarketcapItem(scrapy.Item):

    id = scrapy.Field()
    name = scrapy.Field()
    symbol = scrapy.Field()
    rank = scrapy.Field()
    price_usd = scrapy.Field()
    price_btc = scrapy.Field()
    s24h_volume_usd = scrapy.Field()
    market_cap_usd = scrapy.Field()
    available_supply = scrapy.Field()
    total_supply = scrapy.Field()
    max_supply = scrapy.Field()
    percent_change_1h = scrapy.Field()
    percent_change_24h = scrapy.Field()
    percent_change_7d = scrapy.Field()
    last_updated = scrapy.Field()


class EthSysWhaleItem(scrapy.Item):
    quantity = scrapy.Field()
    address = scrapy.Field()
    symbol = scrapy.Field()
    timestamp = scrapy.Field()
    name = scrapy.Field()



