import time
from datetime import datetime, timedelta
from data_fetch import fetch_stock_data
from momentum_screening import screen_stocks
from risk_parity import calculate_volatility, risk_parity_allocation

def rebalance_portfolio(stocks, rebalance_frequency=7):
    """
    Rebalance the portfolio every `rebalance_frequency` days.
    """
    end_date = datetime.now() + timedelta(days=90)  # Competition ends in 3 months
    while datetime.now() < end_date:
        # Fetch data
        stock_data = fetch_stock_data(stocks)
        
        # Screen stocks
        screened_stocks = screen_stocks(stock_data)
        
        # Calculate volatility for screened stocks
        for symbol, df in screened_stocks.items():
            df = calculate_volatility(df)
            screened_stocks[symbol] = df
        
        # Get volatilities for screened stocks
        screened_volatilities = {symbol: df['Volatility'].iloc[-1] for symbol, df in screened_stocks.items()}
        
        # Perform risk parity allocation
        weights = risk_parity_allocation(list(screened_volatilities.values()))
        allocations = {symbol: weight for symbol, weight in zip(screened_stocks.keys(), weights)}
        
        print(f"🔄 Rebalanced Portfolio on {datetime.now().strftime('%Y-%m-%d')}:")
        for symbol, allocation in allocations.items():
            print(f"{symbol}: {allocation:.2%}")
        
        # Wait for the next rebalance
        time.sleep(rebalance_frequency * 86400)  # Convert days to seconds