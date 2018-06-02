# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
# from redis import StrictRedis
from urllib import parse
from pymongo import MongoClient


class TokensSpider(scrapy.Spider):
    name = 'tokens'
    allowed_domains = ['etherscan.io']
    start_urls = ['http://etherscan.io/tokens/']
    # redis = StrictRedis(host='192.168.1.8', port=6379, db=0)
    conn = MongoClient('192.168.1.8', 27017)
    db = conn.contract_address
    myset = db.eth

    def parse(self, response):

        address_tags = response.css("td.hidden-xs a[href]").extract()

        # price = response.css("table.table tr > td:nth-child(5) > span::text").extract()
        # price_btc = response.css("table.table tr > td:nth-child(5) >font::text").extract()
        for index in range(len(address_tags)):
            if index % 2 != 0:
                address_tag = address_tags[index]
                match_re = re.match('.+token/(.+)">(.+)\((.+)\)</a>', address_tag)
                if match_re:
                    address = match_re.group(1)
                    symbol_name = match_re.group(2)
                    symbol = match_re.group(3)
                    if self.myset.find({"address": address}).count() == 0:
                        self.myset.insert({"address": address, "symbol": symbol, "symbol_name": symbol_name.strip()})
        if self.myset.find({"symbol": "EXC"}).count() == 0:
            self.myset.insert({"address": "0x00c4b398500645eb5da00a1a379a88b11683ba01", "symbol": "EXC", "symbol_name": "Eximchain"})
        if self.myset.find({"symbol": "LBA"}).count() == 0:
            self.myset.insert({"address": "0xfe5f141bf94fe84bc28ded0ab966c16b17490657", "symbol": "LBA",
                               "symbol_name": "LibraToken"})
        next_url = response.css("a.btn.btn-default.btn-xs.logout::attr(href)").extract_first()
        if next_url:
            yield Request(url=parse.urljoin("http://etherscan.io/", next_url), callback=self.parse)

