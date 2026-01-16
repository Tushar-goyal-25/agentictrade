import asyncio
import sys
import os

# Add parent directory to path so we can import from data/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.dataLodaer import getMarketData
from data.strategies import MomentumStrategy, MeanReversionStrategy, MovingAverageCrossoverStrategy, BreakoutStrategy
from backtest import BackTester

class RiskParams:
    max_position_pct = 0.15

async def main():
    symbol = 'TSLA'
    lookback_days = 180
    historical_data =  await getMarketData(symbol, lookback_days)
    # print(historical_data)
    backtest = BackTester(10000, 2)
    momentumstrat = MomentumStrategy()
    mean = MeanReversionStrategy()
    mov = MovingAverageCrossoverStrategy()
    breaks = BreakoutStrategy()
    risk_params = RiskParams()

    # Debug: Check how many days we actually have


    backtest.runBacktest(mean, symbol, historical_data, risk_params)

    
    print(f"\nOpen positions: {len(backtest.positions)}")

# Calculate total portfolio value
    portfolio_value = backtest.cash
    if backtest.positions:
        last_price = historical_data['close'].iloc[-1]
        for sym, pos in backtest.positions.items():
            position_value = pos['shares'] * last_price
            portfolio_value += position_value
            print(f"  {sym}: {pos['shares']:.2f} shares @ ${pos['entry_price']:.2f}")

    print(f"\nPortfolio value: ${portfolio_value:,.2f}")
    print(f"Total return: {(portfolio_value - 10000) / 10000 * 100:+.2f}%")

    # Trade breakdown
    buy_trades = [t for t in backtest.trades if t['action'] == 'BUY']
    sell_trades = [t for t in backtest.trades if t['action'] == 'SELL']
    print(f"\nBUY trades: {len(buy_trades)}")
    print(f"SELL trades: {len(sell_trades)}")

    if sell_trades:
        total_pnl = sum(t['pnl'] for t in sell_trades)
        print(f"Total P&L from closed trades: ${total_pnl:,.2f}")

if __name__ == "__main__":
    asyncio.run(main())
