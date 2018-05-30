# -*- coding: utf-8 -*-
from datetime import datetime
import re
from scrapy.http import Request
import scrapy
from redis import StrictRedis

from TokenTransfers.commons import get_holder_name
from TokenTransfers.items import TokenTopHistoryItem


class EthsystopholderSpider(scrapy.Spider):
    name = 'EthSysTopHolder'
    allowed_domains = ['etherscan.io']
    start_urls = []
    redis = StrictRedis(host='192.168.1.8', port=6379, db=0)
    tokens_names = {}
    tokens_address = {}

    def __init__(self):

        tokens = self.redis.smembers("ETH_TOKENS")
        for token in tokens:
            spilt = token.decode("utf-8").split("=")
            symbol = spilt[0]
            address = spilt[1]
            self.tokens_address[address] = symbol
            self.start_urls.append("https://etherscan.io/token/" + address)
            # break #TODO

        _tokens_names = self.redis.smembers("ETH_TOKENS_NAME")
        for _tokens_name in _tokens_names:
            spilt = str(_tokens_name.decode("utf-8")).split("=")
            name = spilt[0]
            token = str(spilt[1])
            self.tokens_names[name] = token

    def parse(self, response):
        total_supply = response.css("table.table tr > td:nth-child(2)::text").extract()[0].strip().replace(',', '')
        match_re = re.match('^\d+$', total_supply)
        if match_re:
            total_supply = total_supply
            symbol = response.css("table.table tr > td:nth-child(2)::text").extract()[1].strip().replace(',', '')
            symbol_match_re = re.match('\d+\s([A-Za-z0-9]+)\s\(.+', symbol)
            if symbol_match_re:
                symbol = symbol_match_re.group(1)
        else:

            match_re = re.match('^(\d+)\s([A-Za-z0-9]+)\s\(.+', total_supply)
            if match_re:
                total_supply = match_re.group(1)
                symbol = match_re.group(2)
            else:
                match_re = re.match('^(\d+)\s(.+)\s\(.+', total_supply)
                if match_re:
                    total_supply = match_re.group(1)
                    symbol = match_re.group(2)



        Decimals = response.css("table.table tr > td:nth-child(2)::text").extract()[10].strip()
        contract_address = response.css("tr#ContentPlaceHolder1_trContract > td:nth-child(2) > a::text").extract()[0]

        yield Request(url="https://etherscan.io/token/generic-tokenholders2?a=" + contract_address,
                      meta={'total_supply': float(total_supply), 'symbol': symbol, 'contract_address': contract_address},
                      callback=self.parse_tokentxns, dont_filter=True)

        pass


    def parse_tokentxns(self, response):
        total_supply = response.meta['total_supply']
        symbol = response.meta['symbol']
        contract_address = response.meta['contract_address']

        rank_tags = response.css("table.table tr > td:nth-child(1)::text").extract()
        address_tgas = response.css("table.table tr > td > span:nth-child(1)>a::text").extract()
        quantity_tags = response.css("table.table tr > td:nth-child(3)::text").extract()
        # percentage_tags = response.css("table.table tr > td:nth-child(4)::text").extract()

        tokenTopHistoryItem = TokenTopHistoryItem()
        for index in range(0, len(rank_tags)):
            rank = rank_tags[index]
            address = address_tgas[index]
            quantity = float(quantity_tags[index])
            percentage = round((quantity / total_supply) * 100, 2)
            tokenTopHistoryItem['symbol'] = symbol
            tokenTopHistoryItem['rank'] = rank
            tokenTopHistoryItem['address'] = address
            tokenTopHistoryItem['quantity'] = quantity
            tokenTopHistoryItem['percentage'] = percentage
            tokenTopHistoryItem['timestamp'] = datetime.now()
            name = get_holder_name(self, address, symbol)
            tokenTopHistoryItem['name'] = name
            yield tokenTopHistoryItem
