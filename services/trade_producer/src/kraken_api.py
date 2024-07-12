from typing import List, Dict
import json
from websocket import create_connection

class KrakenWebsocketTradeAPI:
    def __init__(self, product_id: str, URL: str = "wss://ws.kraken.com") -> None:

        self.product_id = product_id
        self.URL = URL

        # Establishing the connection to the Kraken websocket API
        self._ws = create_connection(self.URL)
        print ("Connection established!")

        # Subscribing to the trades for the given product
        self._subscribe(self.product_id)

    def _subscribe(self, product_id: str) -> None:

        print (f'Subscribing to trades for {product_id}')

        # Let's subscribe to the trades
        msg = {
            "method": "subscribe",
            "params": {
                "channel": "trade",
                "symbol": [
                    product_id
                ],
                "snapshot": False
            }
        }

        self._ws.send(json.dumps(msg))
        print ("Connection worked!")

        # Dumping the first two messages from the websocket since they are just subscription responses, not trades
        _ = self._ws.recv()
        _ = self._ws.recv()

    def get_trades(self) -> List[Dict]:

        # mock_trades = [
        #     {
        #         "product_id": "BTC-USD",
        #         "price": 60000,
        #         "volume": 0.01,
        #         "timestamp": 1630000000000,
        #     },

        #     {
        #         "product_id": "BTC-USD",
        #         "price": 59000,
        #         "volume": 0.01,
        #         "timestamp": 1640000000000,
        #     }
        # ]

        #return mock_trades

        message = self._ws.recv()

        if 'heartbeat' in message:
            return []

        #print("Message received: ", message)

        message = json.loads(message)

        # Extract trades from the message['data']
        trades = []
        for trade in message['data']:
            trades.append({
                'product_id': self.product_id,
                'price': trade['price'],
                'volume': trade['qty'],
                'timestamp': trade['timestamp']
            })

        return trades