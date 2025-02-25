import pandas as pd

def calculate_momentum_indicators(df, momentum_window=63):
    """
    Calculate momentum (e.g., 3-month return) and RSI for momentum screening.
    """
    # Calculate momentum as the percentage change over the momentum window
    df['Momentum'] = df['close'].pct_change(periods=momentum_window)
    
    # Calculate RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Generate trading signals
    df['Signal'] = (df['Momentum'] > 0) & (df['RSI'] > 50)  # Momentum > 0 and RSI > 50
    
    return df

def screen_stocks(stock_data):
    """
    Screen stocks using momentum strategy.
    """
    screened_stocks = {}
    
    for symbol, df in stock_data.items():
        df = calculate_momentum_indicators(df)
        if df['Signal'].iloc[-1]:  # Check last row for buy signal
            screened_stocks[symbol] = df  # Store the entire DataFrame
    
    return screened_stocks
