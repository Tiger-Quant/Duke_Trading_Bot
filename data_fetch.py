from ib_insync import *
import pandas as pd
from momentum_screening import screen_stocks

def fetch_stock_data(stocks):
    """
    Fetch historical stock data for a list of symbols.
    """
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)  # Ensure your TWS/Gateway is running

    stock_data = {}

    for symbol in stocks:
        contract = Stock(symbol, 'SMART', 'USD')
        bars = ib.reqHistoricalData(contract, endDateTime='', durationStr='1 Y',
                                    barSizeSetting='1 day', whatToShow='TRADES', useRTH=True)

        df = util.df(bars)
        stock_data[symbol] = df

    ib.disconnect()
    return stock_data
