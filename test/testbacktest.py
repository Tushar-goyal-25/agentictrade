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
    # Universe of stocks to test
    universe = ['TSLA', 'NVDA', 'AMD', 'PLTR', 'COIN', 'SHOP', 'RIOT', 'META']
    lookback_days = 180
    initial_capital = 10000

    # Initialize strategy
    strategy = MomentumStrategy()
    risk_params = RiskParams()

    print("=" * 60)
    print(f"BACKTESTING {strategy.__class__.__name__} ACROSS UNIVERSE")
    print("=" * 60)

    results = []

    # Backtest each symbol in the universe
    for symbol in universe:
        print(f"\n{'='*60}")
        print(f"Testing {symbol}...")
        print(f"{'='*60}")

        try:
            # Get historical data
            historical_data = await getMarketData(symbol, lookback_days)

            if historical_data.empty:
                print(f"❌ No data available for {symbol}")
                continue

            # Run backtest
            backtest = BackTester(initial_capital, 2)
            backtest.runBacktest(strategy, symbol, historical_data, risk_params)

            # Calculate final portfolio value
            portfolio_value = backtest.cash
            if backtest.positions:
                last_price = historical_data['close'].iloc[-1]
                for sym, pos in backtest.positions.items():
                    portfolio_value += pos['shares'] * last_price

            # Calculate metrics
            total_return = (portfolio_value - initial_capital) / initial_capital * 100
            buy_trades = [t for t in backtest.trades if t['action'] == 'BUY']
            sell_trades = [t for t in backtest.trades if t['action'] == 'SELL']
            total_pnl = sum(t['pnl'] for t in sell_trades) if sell_trades else 0

            # Store results
            result = {
                'symbol': symbol,
                'final_value': portfolio_value,
                'total_return': total_return,
                'buy_trades': len(buy_trades),
                'sell_trades': len(sell_trades),
                'total_pnl': total_pnl,
                'open_positions': len(backtest.positions),
                'days_with_positions': len([h for h in backtest.portfolio_history if h['position_value'] > 0])
            }
            results.append(result)

            # Print individual results
            print(f"\n📊 Results for {symbol}:")
            print(f"   Final Value: ${portfolio_value:,.2f}")
            print(f"   Total Return: {total_return:+.2f}%")
            print(f"   Trades: {len(buy_trades)} BUY, {len(sell_trades)} SELL")
            print(f"   Closed P&L: ${total_pnl:,.2f}")
            print(f"   Open Positions: {len(backtest.positions)}")

        except Exception as e:
            print(f"❌ Error testing {symbol}: {e}")
            continue

    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY - ALL SYMBOLS")
    print(f"{'='*60}")
    print(f"{'Symbol':<10} {'Return':<12} {'Final Value':<15} {'Trades':<10} {'P&L':<12}")
    print("-" * 60)

    for r in sorted(results, key=lambda x: x['total_return'], reverse=True):
        print(f"{r['symbol']:<10} {r['total_return']:+.2f}%      ${r['final_value']:>10,.2f}    {r['buy_trades']:>2}/{r['sell_trades']:<2}     ${r['total_pnl']:>9,.2f}")

    # Calculate portfolio-level metrics
    if results:
        avg_return = sum(r['total_return'] for r in results) / len(results)
        best = max(results, key=lambda x: x['total_return'])
        worst = min(results, key=lambda x: x['total_return'])

        print("-" * 60)
        print(f"Average Return: {avg_return:+.2f}%")
        print(f"Best: {best['symbol']} ({best['total_return']:+.2f}%)")
        print(f"Worst: {worst['symbol']} ({worst['total_return']:+.2f}%)")

if __name__ == "__main__":
    asyncio.run(main())
