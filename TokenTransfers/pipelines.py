# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from TokenTransfers.models.es_types import TokenTransferType, TokenTopHistoryType, coinmarketcapType


class TokentransfersPipeline(object):
    def process_item(self, item, spider):
        return item


class ElasticsearchPipeline(object):

    def process_item(self, item, spider):
        if spider.name == 'tokenholder':
            token_transfer = TokenTransferType()
            token_transfer.symbol = item['symbol']
            token_transfer.symbol_address = item['symbol_address']
            token_transfer.token_name = item['token_name']
            token_transfer.from_address = item['from_address']
            token_transfer.to_address = item['to_address']
            token_transfer.num = item['num']
            token_transfer.in_or_out = item['in_or_out']
            token_transfer.transfer_token = item['transfer_token']
            token_transfer.date = item['date']
            token_transfer.is_ex_address = item['is_ex_address']
            # token_transfer.percent = item['percent']

            token_transfer.save()

        spiders = ['BTCtokenTopHolder', 'BCHtokenTopHolder']

        if spider.name in spiders:
            token_transfer = TokenTopHistoryType()
            token_transfer.symbol = item['symbol']
            token_transfer.name = item['name']
            token_transfer.address = item['address']
            token_transfer.quantity = item['quantity']
            token_transfer.rank = item['rank']
            token_transfer.percentage = item['percentage']
            token_transfer.timestamp = item['timestamp']
            token_transfer.transaction = item['transaction']
            token_transfer.last_transaction = item['last_transaction']
            token_transfer.save()

        spiders = ['NeblTopHolder', 'EthSysTopHolder', 'EthTopHolder']

        if spider.name in spiders:
            token_transfer = TokenTopHistoryType()
            token_transfer.symbol = item['symbol']
            token_transfer.name = item['name']
            token_transfer.address = item['address']
            token_transfer.quantity = item['quantity']
            token_transfer.rank = item['rank']
            token_transfer.percentage = item['percentage']
            token_transfer.timestamp = item['timestamp']
            token_transfer.save()

        if spider.name == 'CoinMarketCapHistory':
            coinmarketcap = coinmarketcapType()
            coinmarketcap.id = item['id']
            coinmarketcap.name = item['name']
            coinmarketcap.symbol = item['symbol']
            coinmarketcap.rank = item['rank']
            coinmarketcap.price_usd = item['price_usd']
            coinmarketcap.price_btc = item['price_btc']
            coinmarketcap.s24h_volume_usd = item['s24h_volume_usd']
            coinmarketcap.market_cap_usd = item['market_cap_usd']
            coinmarketcap.available_supply = item['available_supply']
            coinmarketcap.total_supply = item['total_supply']
            coinmarketcap.max_supply = item['max_supply']
            coinmarketcap.percent_change_1h = item['percent_change_1h']
            coinmarketcap.percent_change_24h = item['percent_change_24h']
            coinmarketcap.percent_change_7d = item['percent_change_7d']
            coinmarketcap.last_updated = item['last_updated']
            coinmarketcap.save()

        return item


