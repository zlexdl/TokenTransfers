from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text, Boolean, Float
from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["192.168.1.8"])


class TokenTransferType(DocType):
    symbol = Keyword()
    symbol_address = Keyword()
    token_name = Keyword()
    from_address = Keyword()
    to_address = Keyword()
    num = Float()
    in_or_out = Keyword()
    transfer_token = Keyword()
    date = Date()
    is_ex_address = Boolean()
    # percent = Float()
    # rank = Integer()

    class Meta:
        index = "token_transfer"
        doc_type = "transfer"

class TokenTopHistoryType(DocType):
    symbol = Keyword()
    name = Keyword()
    address = Keyword()
    quantity = Float()
    rank = Integer()
    percentage = Float()
    timestamp = Date()
    transaction = Date()
    last_transaction = Date()
    class Meta:
        index = "token_top_history_2"
        doc_type = "token_top"

class coinmarketcapType(DocType):
    id = Keyword()
    name = Keyword()
    symbol = Keyword()
    rank = Integer()
    price_usd = Float()
    price_btc = Float()
    s24h_volume_usd = Float()
    market_cap_usd = Float()
    available_supply = Float()
    total_supply = Float()
    max_supply = Float()
    percent_change_1h = Float()
    percent_change_24h = Float()
    percent_change_7d = Float()
    last_updated = Date()

    class Meta:
        index = "coin_market_cap_history"
        doc_type = "data"

class EthsyswhaleholderType(DocType):
    quantity = Float()
    address = Keyword()
    symbol = Keyword()
    timestamp = Date()
    name = Keyword()

    class Meta:
        index = "ethsys_whale_history"
        doc_type = "data"

if __name__ == "__main__":
    TokenTransferType.init()
    TokenTopHistoryType.init()

