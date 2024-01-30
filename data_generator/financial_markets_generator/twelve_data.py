import requests
from typing import List, Tuple
from data_generator.financial_markets_generator.base_financial_markets_generator.base_financial_markets_generator import BaseFinancialMarketsGenerator

class TwelveData(BaseFinancialMarketsGenerator):
    def __init__(self, api_key):
        super().__init__()
        self._api_key = api_key
        self._symbols = {
            "BTCUSD": "BTC/USD"
        }
        self._tf = {
            5: "5min"
        }

    def _fetch_data(self, symbol, interval, output_size, exchange='coinbase pro'):
        url = f'https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&outputsize={output_size}&apikey={self._api_key}&exchange={exchange}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['values']
        else:
            raise Exception("Error fetching data from TwelveData")

    def get_data(self, symbol: str, tf: int, start: int, end: int, output_size: int = 1000):
        if symbol in self._symbols:
            symbol = self._symbols[symbol]
        if tf in self._tf:
            interval = self._tf[tf]
        else:
            raise Exception("No mapping for TwelveData interval")

        aggregated_data = []
        for exchange in ['coinbase pro', 'binance']:
            data = self._fetch_data(symbol, interval, output_size, exchange)
            for item in data:
                timestamp = int(item['datetime'])  # Convert datetime to timestamp if necessary
                if start <= timestamp <= end:
                    aggregated_data.append(item)

        return aggregated_data

    def get_data_and_structure_data_points(self, symbol: str, tf: int, data_structure: List[List], ts_range: Tuple[int, int]):
        if symbol in self._symbols:
            symbol = self._symbols[symbol]
        if tf in self._tf:
            interval = self._tf[tf]
        else:
            raise Exception("No mapping for TwelveData interval")

        # Fetch data for each exchange and aggregate
        aggregated_data = []
        for exchange in ['coinbase pro', 'binance']:
            data = self._fetch_data(symbol, interval, output_size=1000, exchange=exchange)  # Assuming output_size is fixed
            for item in data:
                timestamp = int(item['datetime'])  # Convert datetime to timestamp if necessary
                if ts_range[0] <= timestamp <= ts_range[1]:
                    aggregated_data.append(item)

        # Convert and structure the data
        # Assuming data_structure and the format required by your system
        # Example: data_structure = [[timestamp, close, high, low, volume], ...]
        for item in aggregated_data:
            data_point = [int(item['datetime']),  # Convert datetime to timestamp
                          float(item['close']),
                          float(item['high']),
                          float(item['low']),
                          float(item['volume'])]  # Assuming volume is required
            data_structure.append(data_point)

        return data_structure