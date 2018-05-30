# -*- coding: utf-8 -*-
import scrapy
from redis import StrictRedis
from scrapy.http import Request
import re
from urllib import parse
import datetime
from TokenTransfers.items import TokentransfersItem


class TokenholderSpider(scrapy.Spider):
    name = 'tokenholder'
    allowed_domains = ['etherscan.io']
    start_urls = []
    redis = StrictRedis(host='192.168.1.8', port=6379, db=0)
    tokens_names = {}
    tokens_address = {}
    ex_address = {'0x8d12a197cb00d4747a1fe03395095ce2a5cc6819': 'etherdelta_2'
                    , '0xa12431d0b9db640034b0cdfceef9cce161e62be4': 'EX1'
                    , '0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208': 'IDEX_1'
                    , '0x2b5634c42055806a59e9107ed44d43c426e58258': 'EX2'
                    , '0x236f9f97e0e62388479bf9e5ba4889e46b0273c3': 'EX3'
                    , '0x3f5ce5fbfe3e9af3971dd833d26ba9b5c936f0be': 'BinanceWallet'
                    , '0xfe9e8709d3215310075d67e3ed32a380ccf451c8': 'BinanceWallet_3'
                    , '0xfbb1b73c4f0bda4f67dca266ce6ef42f520fbb98': 'Bittrex'
                    , '0x05ee546c1a62f90d7acbffd6d846c9c54c7cf94c': 'EX4'
                    , '0x0681d8db095565fe8a346fa0277bffde9c0edbbf': 'EX5'
                    , '0x564286362092d8e7936f0549571a803b203aaced': 'BinanceWallet_2'
                    , '0xd551234ae421e3bcba99a0da6d736074f22192ff': 'BinanceWallet_1'
                    , '0x2984581ece53a4390d1f568673cf693139c97049': 'EX6'
                    , '0x15ab2321d7e83d00c015048b567f4f6aadc1b022': 'BinanceWallet_4'
                    , '0x5e575279bf9f4acf0a130c186861454247394c06': 'liqui.io_Erc20'
                    , '0x4b01721f0244e7c5b5f63c20942850e447f5a5ee': 'coinexchange.io'
                    , '0xeee28d484628d41a82d01e21d12e2e78d69920da': 'EX7'
                    , '0x6cc5f688a315f3dc28a7781717a9a798a59fda7b': 'EX8'
                    , '0xe93381fb4c4f14bda253907b18fad305d799241a': 'EX9'
                    , '0xfdb16996831753d5331ff813c29a93c76834a0ad': 'EX10'
                    , '0x59a5208b32e627891c389ebafc644145224006e8': 'HitBTC_2'
                    , '0xadb2b42f6bd96f5c65920b9ac88619dce4166f94': 'EX11'
                    , '0x03747f06215b44e498831da019b27f53e483599f': 'EX12'
                    , '0x5c985e89dde482efe97ea9f1950ad149eb73829b': 'EX13'
                    , '0x46705dfff24256421a05d056c29e81bdc09723b8': 'EX14'
                    , '0xab5c66752a9e8167967685f1450532fb96d5d24f': 'EX15'
                    , '0x1062a747393198f70f71ec65a582423dba7e5ab3': 'EX16'
                    , '0xf4b51b14b9ee30dc37ec970b50a486f37686e2a8': 'Bitfinex_Wallet'
                    , '0xa30d8157911ef23c46c0eb71889efe6a648a41f7': 'EX17'
                    , '0xf73c3c65bde10bf26c2e1763104e609a41702efe': 'EX18'
                    , '0x6748f50f686bfbca6fe8ad62b22228b87f31ff2b': 'EX19'
                    , '0xfa4b5be3f2f84f56703c42eb22142744e95a2c58': 'EX20'
                    , '0xe03c23519e18d64f144d2800e30e81b0065c48b5': 'EX21'
                    , '0xf07232bc85d995c32c1edf1c985c84a8b7b0ded7': 'EX22'
                    , '0x41d5233f434d98b73f22ce664d48be06f4eb073f': 'EX23'
                    , '0x0a73573cf2903d2d8305b1ecb9e9730186a312ae': 'Tidex-Tokens'
                    , '0x8958618332df62af93053cb9c535e26462c959b0': 'CobinhoodWallet'
                    , '0x0d6b5a54f940bf3d52e438cab785981aaefdf40c': 'Coss.io'
                    , '0x0000000000000000000000000000000000000000': 'EX0'
                    , '0x876eabf441b2ee5b5b0554fd502a8e0600950cfa': 'Bitfinex_Wallet4'
                    , '0xb726da4fbdc3e4dbda97bb20998cf899b0e727e0': 'EX24'
                    , '0x30146933a3a0babc74ec0b3403bec69281ba5914': 'EX25'
                    , '0x304cc179719bc5b05418d6f7f6783abe45d83090': 'EX26'
                    , '0x80a909968642f7f90686ff964e71154a00ce6e49': 'EX27'
                    , '0x7b74c19124a9ca92c6141a2ed5f92130fc2791f2': 'EX28'
                    , '0x5bd387c00ec5b4999800cf1223be1205aaa3a321': 'Hack'}

    done_address = []

    def __init__(self):

        tokens = self.redis.smembers("ETH_TOKENS")
        for token in tokens:
            spilt = token.decode("utf-8").split("=")
            symbol = spilt[0]
            address = spilt[1]
            self.tokens_address[address] = symbol
            self.start_urls.append("http://etherscan.io/token/generic-tokenholders2?a=" + address)

        _tokens_names = self.redis.smembers("ETH_TOKENS_NAME")
        for _tokens_name in _tokens_names:
            spilt = str(_tokens_name.decode("utf-8")).split("=")
            name = spilt[0]
            token = str(spilt[1])
            self.tokens_names[name] = token

    def parse(self, response):
        url = response.url
        match_re = re.match('.+\?a=(0x.{40}).*', url)
        if match_re:
            token_address = match_re.group(1)

        address_tags = response.css("span a::attr(href)").extract()
        for address_tag in address_tags:
            match_re = re.match('/token/.+\?a=(0x.{40})', address_tag)
            if match_re:
                address = match_re.group(1)
                # address is ex_address?
                if address in self.ex_address.keys():
                    is_ex_address = True
                    continue # TODO
                else:
                    is_ex_address = False

                if token_address in self.tokens_address.keys():
                    symbol = self.tokens_address[token_address]
                    # tokentxns_address = "https://etherscan.io/tokentxns?a=" + address
                    if address not in self.done_address:
                        self.done_address.append(address)
                        yield Request(url="https://etherscan.io/tokentxns?a=" + address,
                                      meta={'address': token_address, 'symbol': symbol, 'is_ex_address': is_ex_address},
                                      callback=self.parse_tokentxns, dont_filter=True)

            # print(address)

        pass

    def parse_tokentxns(self, response):
        symbol = response.meta['symbol']
        symbol_address = response.meta['address']
        is_ex_address = response.meta['is_ex_address']

        token_transfer = TokentransfersItem()
        dates = response.css("span::attr(title)").extract()
        addresses = response.css("span.address-tag").extract()
        in_or_outs = response.css("span.label::text").extract()
        values = response.css("tr>td:nth-child(6n)::text").extract()
        tokens = response.css("tr>td:nth-child(7n)>a::text").extract()
        for index in range(len(dates)):
            date = dates[index]

            _from_address = addresses[3 * (index + 1) - 2]
            from_address = self.get_address_from_response(_from_address)
            _to_address = addresses[3 * (index + 1) - 1]
            to_address = self.get_address_from_response(_to_address)
            in_or_out = str(in_or_outs[index]).strip('\xa0 ')
            num = float(values[index].replace(',', ''))
            token_name = tokens[index].strip()
            transfer_token = ''
            dict_tokens_names = self.tokens_names
            if token_name in dict_tokens_names.keys():
                transfer_token = dict_tokens_names[token_name]
            else:
                if token_name.find('Erc20') > -1:
                    transfer_token = token_name.replace('Erc20 (', '').replace(')', '')
                # self.redis.sadd(token_name) #TODO

            token_transfer['symbol'] = symbol
            token_transfer['symbol_address'] = symbol_address
            token_transfer['token_name'] = token_name
            token_transfer['from_address'] = from_address
            token_transfer['to_address'] = to_address
            token_transfer['num'] = num
            token_transfer['in_or_out'] = in_or_out
            token_transfer['transfer_token'] = transfer_token
            token_transfer['date'] = date
            token_transfer['is_ex_address'] = is_ex_address
            ####################################
            now = datetime.datetime.now()
            d1 = now - datetime.timedelta(days=30)
            if datetime.datetime.strptime(str(date), '%b-%d-%Y %H:%M:%S %p') <= d1.replace(hour=0, minute=0, second=0, microsecond=0):
                continue
            if datetime.datetime.strptime(str(date), '%b-%d-%Y %H:%M:%S %p') > now.replace(hour=0, minute=0, second=0, microsecond=0):
                continue
            ####################################
            if transfer_token not in self.tokens_address.values():
                continue
            ####################################
            yield token_transfer

        next_url = response.css("a.btn.btn-default.btn-xs.logout::attr(href)").extract_first()
        if next_url:
            yield Request(url=parse.urljoin("http://etherscan.io/", next_url),
                          meta={'address': symbol_address, 'symbol': symbol, 'is_ex_address': is_ex_address},
                          callback=self.parse_tokentxns, dont_filter=True)
        pass

    def get_address_from_response(self, address):
        aexist_address = address.find('</a>')
        if aexist_address > 0:
            match_re = re.match('.+>(0x.+)<\/a.+', address)
            if match_re:
                return match_re.group(1)
            else:
                match_re = re.match('.+>(.+)<\/a.+', address)
                if match_re:
                    return match_re.group(1)
                else:
                    return
        else:
            match_re = re.match('.+>(.+)<.+', address)
            if match_re:
                return match_re.group(1)
            else:
                return


