# backtest.py
import pandas as pd
from momentum_screening import calculate_momentum_indicators, screen_stocks
from risk_parity import calculate_volatility, risk_parity_allocation

def backtest_strategy(stock_data, start_date, end_date, rebalance_frequency=7):
    """
    Backtest the momentum + risk parity strategy.
    """
    # Initialize portfolio
    portfolio_value = 10000  # Starting capital
    portfolio = {}  # Tracks holdings and cash

    # Convert stock_data to a dictionary of DataFrames
    stock_data = {symbol: df[(df['date'] >= start_date) & (df['date'] <= end_date)] 
                  for symbol, df in stock_data.items()}

    # Main backtesting loop
    current_date = pd.to_datetime(start_date)
    while current_date <= pd.to_datetime(end_date):
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

        # Update portfolio value
        portfolio_value = update_portfolio(portfolio, allocations, stock_data, current_date)

        # Log performance
        print(f"📅 Date: {current_date.strftime('%Y-%m-%d')}")
        print(f"💰 Portfolio Value: ${portfolio_value:.2f}")
        for symbol, allocation in allocations.items():
            print(f"{symbol}: {allocation:.2%}")

        # Move to the next rebalance date
        current_date += pd.Timedelta(days=rebalance_frequency)

    return portfolio_value

def update_portfolio(portfolio, allocations, stock_data, current_date):
    """
    Update portfolio holdings and value based on allocations.
    """
    portfolio_value = 0
    for symbol, allocation in allocations.items():
        price = stock_data[symbol][stock_data[symbol]['date'] == current_date]['close'].values[0]
        portfolio[symbol] = allocation * portfolio_value / price
        portfolio_value += portfolio[symbol] * price

    return portfolio_value

# Example usage
if __name__ == "__main__":
    # Load historical data (replace with your data fetching logic)
    stock_data = {
        'AAPL': pd.read_csv('AAPL.csv'),  # Replace with actual data
        'META': pd.read_csv('META.csv'),  # Replace with actual data
        'NFLX': pd.read_csv('NFLX.csv'),  # Replace with actual data
    }

    # Define backtest period
    start_date = '2022-01-01'
    end_date = '2022-12-31'

    # Run backtest
    final_value = backtest_strategy(stock_data, start_date, end_date)
    print(f"🏁 Final Portfolio Value: ${final_value:.2f}")