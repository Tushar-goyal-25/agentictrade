
from math import sqrt
from statistics import mean, stdev
import backtest

class Metrics:
    def __init__(self, backtest):
        self.portfolio_history = backtest.portfolio_history
        self.trades = backtest.trades
        self.initial_capital = backtest.initial_captial

    
    def calculate(self):
        values = [entry['total_value']for entry in self.portfolio_history]
        daily_returns = []
        for i in range(1,len(values)):
            prev_value = values[i-1]
            curr_value = values[i]
            daily_return = (curr_value-prev_value)/ prev_value
            daily_returns.append(daily_return)
        avg_daily_return = mean(daily_returns)
        annualized_return = avg_daily_return *252 #Trading days per year 
        volatility_daily = stdev(daily_returns)
        annualized_volatility = volatility_daily * sqrt(252) #volatlity scales with square root of time 

        risk_free_rate = 0.02
        sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility
        return sharpe_ratio
        


