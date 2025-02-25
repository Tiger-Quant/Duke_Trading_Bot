import numpy as np
from scipy.optimize import minimize

def calculate_volatility(df, window=21):
    """
    Calculate annualized volatility for each stock.
    """
    returns = df['close'].pct_change()
    df['Volatility'] = returns.rolling(window=window).std() * np.sqrt(252)  # Annualized
    return df

def risk_parity_allocation(volatilities):
    """
    Allocate capital using risk parity.
    """
    n = len(volatilities)
    initial_weights = np.ones(n) / n  # Start with equal weights
    bounds = [(0, 1) for _ in range(n)]  # Weights between 0% and 100%
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})  # Sum of weights = 100%

    def risk_parity_objective(weights):
        risk_contributions = weights * volatilities
        return np.sum((risk_contributions - np.mean(risk_contributions)) ** 2)  # Minimize variance of risk contributions

    result = minimize(risk_parity_objective, initial_weights, bounds=bounds, constraints=constraints)
    return result.x