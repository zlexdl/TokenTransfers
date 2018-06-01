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

        # address_tags = response.css("td.hidden-xs a::attr(href)").extract()
        address_tags = response.css("td.hidden-xs a[href]").extract()
        #response.css("table.table tr > td:nth-child(3) >h5 > a::text").extract() #list 'Tronix (TRX)'

        price = response.css("table.table tr > td:nth-child(5) > span::text").extract()
        price_btc = response.css("table.table tr > td:nth-child(5) >font::text").extract()
        for index in range(len(address_tags)):
            if index % 2 != 0:
                address_tag = address_tags[index]
                match_re = re.match('.+token/(.+)">(.+)\((.+)\)</a>', address_tag)
                if match_re:
                    address = match_re.group(1)
                    symbol_name = match_re.group(2)
                    symbol = match_re.group(3)
                    self.myset.save({"address": address, "symbol": symbol, "symbol_name": symbol_name.strip()})
        #             self.redis.sadd("ETH_TOKENS", symbol + "=" + address)
        #             self.redis.sadd("ETH_TOKENS_NAME", symbol_name.strip() + "=" + symbol)
        # self.redis.sadd("ETH_TOKENS","LBA=0xfe5f141bf94fe84bc28ded0ab966c16b17490657")
        # self.redis.sadd("ETH_TOKENS","EXC=0x00c4b398500645eb5da00a1a379a88b11683ba01")
        next_url = response.css("a.btn.btn-default.btn-xs.logout::attr(href)").extract_first()
        # if next_url:
        yield Request(url=parse.urljoin("http://etherscan.io/", next_url), callback=self.parse)
        # else:
        #     self.redis.save()

    # def parse_detail(self, response):
    #     address_tags = response.css("span a::attr(href)").extract()
    #     for address_tag in address_tags:
    #         match_re = re.match('/token/(.+)\?a.+', address_tag)
    #         if match_re:
    #             address = match_re.group(1)
    #             # tokentxns_address = "https://etherscan.io/tokentxns?a=" + address
    #             yield Request(url="https://etherscan.io/tokentxns?a=" + address,
    #                           callback=self.parse_tokentxns, dont_filter=True)
    #
    #         # print(address)
    #
    #     pass
    #
    #
    # def parse_tokentxns(self, response):
    #     date = response.css("span::attr(title)").extract()
    #     from_address = response.css("span .address-tag").extract()
    #     in_or_out = response.css("span .label label-orange rounded").extract()
    #
    #     pass
