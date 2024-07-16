import requests
from loguru import logger
from quixstreams import Application

from src import config
from src.kraken_api import KrakenWebsocketTradeAPI


# Creates a Kraken product_id from the first_part and second_part of the assets pairs in case of Bitcoin, since
# in Kraken the first_part is always 'XBT' for Bitcoin. Otherwise, it takes the wsname from the asset_pairs_url
def create_kraken_pair(first_part, second_part, wsname):
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
                crypto_pairs.append(
                    create_kraken_pair(first_part[1:], second_part[1:], data['wsname'])
                )

    return crypto_pairs


def produce_trades(
    kafka_broker_address: str,  # Address of the Kafka broker
    kafka_topic_name: str,  # Name of the Kafka topic
    product_id: list,  # The product ID
    URL: str,  # The URL of the Kraken websocket API, e.g. 'wss://ws.kraken.com'
) -> None:
    """
    Read trades from the Kraken websocket API and saves them into a Kafka topic.

    Args:
        kafka_broker_address (str): The address of the Kafka broker
        kafka_topic_name (str): The name of the Kafka topic

    Returns:
        None
    """
    # Create a new Quix application
    app = Application(broker_address=kafka_broker_address)

    # The topic where we will save the trades
    topic = app.topic(name=kafka_topic_name, value_serializer='json')

    kraken_api = KrakenWebsocketTradeAPI(product_id=product_id, URL=URL)

    logger.info('Creating the producer...')

    # Create a Producer instance
    with app.get_producer() as producer:
        while True:
            trades = kraken_api.get_trades()

            for trade in trades:
                # Serialize an event using the defined Topic
                message = topic.serialize(key=trade['product_id'], value=trade)

                # Produce a message into the Kafka topic
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                # Wait for 1 second before producing the next message
                logger.info('Message sent!')
                from time import sleep

                sleep(1)


if __name__ == '__main__':
    produce_trades(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic_name=config.kafka_topic_name,
        product_id=get_crypto_pairs(config.asset_pairs_kraken_url),
        URL=config.URL_KRAKEN,
    )
