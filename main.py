from data_fetch import fetch_stock_data
from momentum_screening import screen_stocks
from risk_parity import calculate_volatility, risk_parity_allocation
from portfolio_manager import rebalance_portfolio

# List of stocks to trade
stocks = ['AAPL', 'MSFT', 'NVDA', 'TSLA', 'AMZN', 'GOOGL', 'META', 'NFLX', 'AMD', 'DIS']

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

# Print risk parity allocations
print("📊 Risk Parity Allocations:")
for symbol, allocation in allocations.items():
    print(f"{symbol}: {allocation:.2%}")

# Start rebalancing
rebalance_portfolio(stocks)