# fetch_historical_data.py (updated with error handling)
from ib_insync import *
import pandas as pd

def fetch_historical_data(symbols, start_date, end_date):
    """
    Fetch historical data for a list of symbols using Interactive Brokers.
    """
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)  # Ensure your TWS/Gateway is running

    stock_data = {}
    for symbol in symbols:
        try:
            contract = Stock(symbol, 'SMART', 'USD')
            bars = ib.reqHistoricalData(
                contract,
                endDateTime=end_date + ' 23:59:59',  # Add time to the end date
                durationStr='1 Y',  # Adjust as needed
                barSizeSetting='1 day',
                whatToShow='TRADES',
                useRTH=True,
                formatDate=1
            )
            if bars:  # Check if data is returned
                df = util.df(bars)
                df['date'] = pd.to_datetime(df['date'])
                stock_data[symbol] = df
            else:
                print(f"⚠️ No data returned for {symbol}")
        except Exception as e:
            print(f"⚠️ Error fetching data for {symbol}: {e}")

    ib.disconnect()
    return stock_data

# Example usage
if __name__ == "__main__":
    # List of stocks to fetch
    symbols = ['AAPL', 'META', 'NFLX']

    # Define date range
    start_date = '20220101'  # YYYYMMDD format
    end_date = '20221231'    # YYYYMMDD format

    # Fetch historical data
    stock_data = fetch_historical_data(symbols, start_date, end_date)

    # Save data to CSV files
    for symbol, df in stock_data.items():
        df.to_csv(f'{symbol}.csv', index=False)