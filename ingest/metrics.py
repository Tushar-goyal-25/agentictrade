
from math import sqrt
from statistics import mean, stdev
import backtest

class Metrics:
    def __init__(self, backtest):
        self.portfolio_history = backtest.portfolio_history
        self.trades = backtest.trades
        self.initial_capital = backtest.initial_captial

    
    def calculatesharperatio(self):
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

    def calculatedrawdown(self):
        peak = self.portfolio_history[0]['total_value']
        max_drawdown = 0 
        max_peak = peak

        for i in self.portfolio_history:
            cur_value = i['total_value']
            if cur_value > peak:
                peak = cur_value 
            drawdown = peak - cur_value
            if drawdown > max_drawdown:
                max_drawdown = drawdown
                max_peak = peak
        max_drawdown_pct = (max_drawdown/ max_peak) *100
        return max_drawdown_pct, max_drawdown

    def calculatetotalreturn(self):
        final_value = self.portfolio_history[-1]['total_value']
        total_return = final_value - self.initial_capital
        total_return_pct = (total_return/self.initial_capital) * 100
        return total_return, total_return_pct
    
    def calculatewinrate(self): 
        total_trades = 0
        winners = 0
        for trades in self.trades:
            if trades['action'] == 'SELL' and trades['pnl'] is not None:
                total_trades += 1
                if trades['pnl'] > 0:
                    winners += 1 
        if total_trades > 0:
            win_rate = (winners / total_trades) * 100
            return win_rate
        else:
            return 0
    
    def calculateprofitfactor(self): 
        gross_profit = 0
        gross_loss = 0
        for trades in self.trades:
            if trades['action'] == 'SELL' and trades['pnl'] is not None:
                if trades['pnl'] > 0:
                    gross_profit = gross_profit + trades['pnl']
                elif trades['pnl'] < 0:
                    gross_loss = gross_loss + abs(trades['pnl'])
        if gross_loss == 0:
            return float('inf') if gross_profit > 0 else 0
        
        profit_factor = gross_profit/ gross_loss
        return profit_factor



