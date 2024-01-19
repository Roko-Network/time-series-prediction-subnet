import requests

class TwelveDataService:
    def __init__(self, api_key):
        self._api_key = api_key

    def fetch_data(self, exchange, symbol, interval, output_size):
        url = f'https://api.twelvedata.com/time_series?exchange={exchange}&symbol={symbol}&interval={interval}&outputsize={output_size}&apikey={self._api_key}'
        response = requests.get(url)
        return response.json()
    
    def calculate_weighted_average(self, data):
        total_volume = sum(item.get('volume', 0) for item in data)
        if total_volume == 0:
            return None  # Avoid division by zero

        weighted_sum = sum(item.get('close', 0) * item.get('volume', 0) for item in data)
        weighted_avg = weighted_sum / total_volume
        return weighted_avg
    
    def get_weighted_avg_close_price(self, symbol, interval, output_size, exchanges):
        aggregated_data = []
        for exchange in exchanges:
            data = self.fetch_data(exchange, symbol, interval, output_size)
            if 'values' in data:
                for item in data['values']:
                    try:
                        close_price = float(item.get('close', 0))
                        volume = float(item.get('volume', 0))
                        print("----------fetch_data-----------------")
                        print(volume)
                        print("---------------------------")
                        if volume > 0:  # Only include data points with volume
                            aggregated_data.append({'close': close_price, 'volume': volume})
                    except (KeyError, ValueError, TypeError) as e:
                        print(f"Error processing data from {exchange}: {e}")

        if not aggregated_data:
            return None

        return self.calculate_weighted_average(aggregated_data)


api_key = "909be1f927ed408ca0c086e23aa20fe5"
service = TwelveDataService(api_key)
weighted_avg_close = service.get_weighted_avg_close_price('BTC/USD', '5min', 100, ['coinbase pro', 'binance'])

print("Weighted Average Closing Price:", weighted_avg_close)
