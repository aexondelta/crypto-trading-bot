import time
import requests
import hmac
import hashlib
import json

# Your Binance API credentials for the testnet
API_KEY = 'your_api_key'
API_SECRET = 'your_secret_key'
BASE_URL = 'https://testnet.binance.vision/api'

def get_historical_data(symbol, interval, start_time, end_time):
    url = f"{BASE_URL}/v3/klines"
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': start_time,
        'endTime': end_time
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

def create_order(symbol, side, type, quantity):
    url = f"{BASE_URL}/v3/order"
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': symbol,
        'side': side,
        'type': type,
        'quantity': quantity,
        'timestamp': timestamp
    }
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    params['signature'] = signature
    headers = {
        'X-MBX-APIKEY': API_KEY
    }
    response = requests.post(url, headers=headers, params=params)
    return response.json()

def run_trading_logic():
    print("Running trading logic...")
    symbol = 'BTCUSDT'
    interval = '1d'
    start_time = 1622505600000  # Example start time
    end_time = 1625097600000  # Example end time
    try:
        historical_data = get_historical_data(symbol, interval, start_time, end_time)
        closes = [float(candle[4]) for candle in historical_data]
        short_avg = sum(closes[-5:]) / 5
        long_avg = sum(closes[-20:]) / 20
        print(f"Short Avg: {short_avg}, Long Avg: {long_avg}")
        if short_avg > long_avg:
            print("Buying BTC")
            create_order(symbol, 'BUY', 'MARKET', 0.001)
        elif short_avg < long_avg:
            print("Selling BTC")
            create_order(symbol, 'SELL', 'MARKET', 0.001)
    except Exception as e:
        print(f"An error occurred: {e}")

while True:
    try:
        run_trading_logic()
    except Exception as e:
        print(f"Error in main loop: {e}")
    time.sleep(3600)  # Sleep for 1 hour
