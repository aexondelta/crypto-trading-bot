import time
import pandas as pd
from binance.client import Client

# Testnet API credentials
API_KEY = 'API_KEY'
API_SECRET = 'API_SECRET'

# Initialize the client for Binance Futures Testnet
client = Client(API_KEY, API_SECRET, testnet=True)
client.API_URL = 'https://testnet.binancefuture.com/fapi'

# List of cryptocurrencies to trade
symbols = [
    'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'XRPUSDT',
    'DOTUSDT', 'UNIUSDT', 'LTCUSDT', 'LINKUSDT', 'BCHUSDT'
]

def get_historical_data(symbol, interval, lookback):
    # Fetch historical data
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=lookback)
    data = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume', 
        'close_time', 'quote_asset_volume', 'number_of_trades', 
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    data['close'] = data['close'].astype(float)
    return data

def calculate_ema(data, span):
    # Calculate Exponential Moving Average (EMA)
    return data['close'].ewm(span=span, adjust=False).mean()

def run_trading_logic():
    # Trading logic for each symbol
    print("Running trading logic...")
    interval = '1h'
    lookback = 50
    short_ema_span = 12
    long_ema_span = 26

    for symbol in symbols:
        try:
            # Fetch historical data
            historical_data = get_historical_data(symbol, interval, lookback)
            
            # Calculate short-term and long-term EMAs
            historical_data['short_ema'] = calculate_ema(historical_data, short_ema_span)
            historical_data['long_ema'] = calculate_ema(historical_data, long_ema_span)
            
            # Get the latest EMA values
            short_ema = historical_data['short_ema'].iloc[-1]
            long_ema = historical_data['long_ema'].iloc[-1]
            
            # Print EMAs for debugging
            print(f"{symbol} - Short EMA: {short_ema}, Long EMA: {long_ema}")
            
            # Example buy/sell logic based on EMA crossover
            if short_ema > long_ema:
                print(f"Buying {symbol}")
                client.futures_create_order(
                    symbol=symbol,
                    side='BUY',
                    type='MARKET',
                    quantity=0.001  # Adjust quantity as needed
                )
            elif short_ema < long_ema:
                print(f"Selling {symbol}")
                client.futures_create_order(
                    symbol=symbol,
                    side='SELL',
                    type='MARKET',
                    quantity=0.001  # Adjust quantity as needed
                )
        except Exception as e:
            print(f"An error occurred for {symbol}: {e}")

while True:
    try:
        run_trading_logic()
    except Exception as e:
        print(f"Error in main loop: {e}")
    time.sleep(3600)  # Sleep for 1 hour

