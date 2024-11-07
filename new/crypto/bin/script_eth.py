#!/usr/bin/env python3

from binance.client import Client
import datetime
import pandas as pd
import os
from dotenv import load_dotenv
from time import sleep

load_dotenv()

# Initialize Binance client

def bin_client():
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
    client = Client(API_KEY, API_SECRET)
    min_to_check = 30

    # Set the symbol and time interval
    symbol = 'ETHUSDT'
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(minutes=min_to_check)

    # Convert times to milliseconds for the API call
    start_time_ms = int(start_time.timestamp() * 1000)
    end_time_ms = int(end_time.timestamp() * 1000)

    # Fetch trades for ETHUSDT within the last 30 minutes
    trades = client.get_aggregate_trades(symbol=symbol,
                                         startTime=start_time_ms,
                                         endTime=end_time_ms)

    # Initialize counters
    buy_count = 0
    sell_count = 0

    # Calculate buy and sell counts
    for trade in trades:
        """'m' is True if the maker is the seller, implying a buy from taker
        """
        if trade['m']:
            buy_count += 1
        else:
            sell_count += 1

    # Calculate buy/sell ratio
    if sell_count > 0:
        buy_sell_ratio = buy_count / sell_count
    else:
        buy_sell_ratio = float('inf')  # If no sells, ratio is infinite
    return {
            'buy_count': buy_count,
            'sell_count': sell_count,
            'buy_sell_ratio': f"{buy_sell_ratio:.2f}"
            }

for i in range(100):
    sleep(10)
    tmp = bin_client()
    print("buy count: {}\nsell count: {}\nbuy to sell ratio: {}\n".format(
          tmp['buy_count'], tmp['sell_count'], tmp['buy_sell_ratio']))
