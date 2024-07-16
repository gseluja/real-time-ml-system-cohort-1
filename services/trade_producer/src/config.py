import requests


# Creates a Kraken product_id from the first_part and second_part of the assets pairs in case of Bitcoin, since
# in Kraken the first_part is always 'XBT' for Bitcoin. Otherwise, it takes the wsname from the asset_pairs_url
def create_kraken_pair(first_part,
                       second_part,
                       wsname):

    if first_part == 'XBT':
        base = 'BTC'
        return f'{base}/{second_part}'
    else:
        return f'{ (wsname) }'

# Retrieves a list of product_ids (assets pairs) from the specified asset_pairs_url.
def get_crypto_pairs(asset_pairs_kraken_url: str):

    pairs = requests.get(asset_pairs_kraken_url).json()['result']
    crypto_pairs = []
    parts_length = 4

    for pair, data in pairs.items():
        if pair[0] == 'X':
            first_part, second_part = pair[:parts_length], pair[parts_length:]
            if second_part == 'ZUSD':
                crypto_pairs.append(create_kraken_pair(first_part[1:], second_part[1:], data['wsname']))

    return crypto_pairs

URL_KRAKEN = 'wss://ws.kraken.com/v2'
asset_pairs_kraken_url = 'https://api.kraken.com/0/public/AssetPairs'
kafka_broker_address = 'redpanda-0:9092'
kafka_topic_name = 'trade'
product_id = get_crypto_pairs(asset_pairs_kraken_url)
