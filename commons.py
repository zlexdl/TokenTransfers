# -*- coding: utf-8 -*-
from datetime import datetime

from redis import StrictRedis

def get_holder_name(self, address, symbol):
    if self.redis.exists(symbol + ':' + address):
        name = self.redis.get(symbol + ':' + address).decode("utf-8")
    else:
        key_counter = symbol + ':counter'
        if not self.redis.exists(key_counter):
            self.redis.set(key_counter, 1)
        else:
            self.redis.incr(key_counter)
        name_no = self.redis.get(key_counter)

        #eth
        if symbol == 'eth':
            if self.redis.exists(symbol + ':' + address):
                name = self.redis.get(symbol + ':' + address).decode("utf-8")
            else:
                name = symbol + '_' + name_no.decode("utf-8").zfill(3)
        else:
            name = symbol + '_' + name_no.decode("utf-8").zfill(3)
        self.redis.set(symbol + ':' + address, name)
        self.redis.save()
    return name


def add_addresses():
    eth_address = {
          '0x8d12a197cb00d4747a1fe03395095ce2a5cc6819': 'etherdelta_2'
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
        , '0x5bd387c00ec5b4999800cf1223be1205aaa3a321': 'Hack'
        , '0xaeec6f5aca72f3a005af1b3420ab8c8c7009bac8': 'EX29'
        , '0xe853c56864a2ebe4576a807d26fdc4a0ada51919': 'Kraken_3'
        , '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae': 'EthDev'
        , '0xf0160428a8552ac9bb7e050d90eeade4ddd52843': 'DigixCrowdSale'
        , '0x9937dbb2128b55c44d8af7bf36fd76796a814cf4': 'EOS-Owner'
        , '0x7da82c7ab4771ff031b66538d2fb9b0b047f6cf9': 'GolemMultisig'
        , '0x3bfc20f0b9afcace800d73d2191166ff16540258': 'Polkadot-Multisig'
        , '0xd0a6e6c54dbc68db5db3a091b171a77407ff7ccf': 'EOSCrowdsale'
        , '0x267be1c1d684f78cb4f6a176c4911b741e4ffdc0': 'Kraken_4'
        , '0xcafe1a77e84698c83ca8931f54a755176ef75f2c': 'Aragon_Multisig'
        , '0xbf4ed7b27f1d666546e30d74d50d173d20bca754': 'WithdrawDAO'
        , '0xc78310231aa53bd3d0fea2f8c705c67730929d8f': 'SingularFunds'
        , '0x851b7f3ab81bd8df354f0d7640efcd7288553419': 'Gnosis-AuctionWallet'
        , '0x0a869d79a7052c7f1b55a8ebabbea3420f0d1e13': 'Kraken_2'
        , '0x376c3e5547c68bc26240d8dcc6729fff665a4448': 'Iconomi-Multisig'
        , '0x4fdd5eb2fb260149a3903859043e962ab89d8ed4': 'Bitfinex_Wallet3'
        , '0x3eb01b3391ea15ce752d01cf3d3f09dec596f650': 'KyberMultiSigWallet'
        , '0xb3764761e297d6f121e79c32a65829cd1ddb4d32': 'MultisigExploit-Hacker'
        , '0xdd76b55ee6dafe0c7c978bff69206d476a5b9ce7': 'RequestNetworkWallet'
        , '0x32be343b94f860124dc4fee278fdcbd38c102d88': 'Poloniex Wallet'
        , '0x755cdba6ae4f479f7164792b318b2a06c759833b': 'ExtraBalDaoWithdraw'
        , '0x1342a001544b8b7ae4a5d374e33114c66d78bd5f': 'GatecoinHack_2'
        , '0xd4914762f9bd566bd0882b71af5439c0476d2ff6': 'GatecoinHack_1'
        , '0xebbd58cd1c31c08ef7a17337c264ba502762e993': 'AirSwapPreSale'
        , '0xc98f8c6b319ecceccaa9361ed5372274674f96cf ': 'FusionWallet'
        , '0xc87b1bf162c1719e3ffdf34995d1853192d6633b': 'DecentBetMultiSigWallet'
        , '0x185f19b43d818e10a31be68f445ef8edcb8afb83': 'TenXMultiSig'
        , '0x9d217bcbd0bfae4d7f8f12c7702108d162e3ab79': 'BloomMultiSigWallet'
        , '0x606af0bd4501855914b50e2672c5926b896737ef': 'ZRX-Org'
        , '0x1706024467ef8c9c4648da6fc35f2c995ac79cf6': 'HeroWallet'
        , '0xd20e4d854c71de2428e1268167753e4c7070ae68': 'district0xMultiSig'
        , '0x04786aada9deea2150deab7b3b8911c309f5ed90': 'GatecoinHack'
        , '0x7e6614722614e434c4df9901bab31e466ba12fa4': 'MysteriumDev'
        , '0xb2930b35844a230f00e51431acae96fe543a0347': 'miningpoolhub_1'
        , '0x00c7122633a4ef0bc72f7d02456ee2b11e97561e': 'RaidenMultiSigWallet'
        , '0xc39e562defc6ddd1f44ee698cf9303092b86051d': 'BancorSplitWallet_3'
        , '0x390de26d772d2e2005c6d1d24afc902bae37a4bb': 'Upbit'
        , '0x2910543af39aba0cd09dbb2d50200b3e800a63d2': 'Kraken_1'
        , '0x7a121269e74d349b5ecfccb9ca948549278d0d10': 'ViceIndustryTokenSale'
        , '0x390de26d772d2e2005c6d1d24afc902bae37a4bb': 'Upbit'
        }
    redis = StrictRedis(host='localhost', port=6379, db=0)

    for address in eth_address.keys():
        key = 'eth:' + address
        value = eth_address[address]
        redis.set(key, value)
    redis.save()

#print (datetime.fromtimestamp(1525090466))
# print (datetime(1525090466))
