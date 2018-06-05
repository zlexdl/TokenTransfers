# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import json
import math
from TokenTransfers.items import EthSysWhaleItem
from pymongo import MongoClient
import re

# scrapy crawl Ethsyswhaleholder -s DOWNLOAD_DELAY=30
class EthsyswhaleholderSpider(scrapy.Spider):
    name = 'Ethsyswhaleholder'
    allowed_domains = ['api.ethplorer.io']
    start_urls = []
    address_name = {}

    def __init__(self):
        conn = MongoClient('192.168.1.8', 27017)
        db = conn.token_address
        token_address = db.eth_ex
        for i in token_address.find():
            name = i["name"]
            address = i["address"]
            self.address_name[address] = name
            self.start_urls.append("https://api.ethplorer.io/getAddressInfo/" + address + "?apiKey=freekey")

    def parse(self, response):
        url = response.url
        symbol_match_re = re.match('.+getAddressInfo\/(.+)\?.+', url)
        if symbol_match_re:
            address = symbol_match_re.group(1)
        name = self.address_name[address]
        main_data = json.loads(response.body.decode("utf-8"))
        item = EthSysWhaleItem()
        tokens = main_data['tokens']
        for index in range(len(tokens)):
            data = tokens[index]
            tokeninfo = data['tokenInfo']
            decimals = tokeninfo['decimals']
            if decimals != '0':
                balance = data['balance']
                item['name'] = name
                item['symbol'] = tokeninfo['symbol']
                item['address'] = tokeninfo['address']
                item['quantity'] = balance / math.pow(10, float(decimals))
                item['timestamp'] = datetime.now()
                yield item
        pass
