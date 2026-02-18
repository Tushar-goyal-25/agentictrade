from flask import Flask, jsonify, request
from flask_cors import CORS
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.dataLodaer import getMarketData
from data.strategies import MomentumStrategy, MeanReversionStrategy, MovingAverageCrossoverStrategy, BreakoutStrategy
from backtest import BackTester
from ingest.metrics import Metrics

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Enable CORS for all API routes

class RiskParams:
    max_position_pct = 0.15

# Strategy mapping
STRATEGIES = {
    'momentum': MomentumStrategy,
    'mean_reversion': MeanReversionStrategy,
    'ma_crossover': MovingAverageCrossoverStrategy,
    'breakout': BreakoutStrategy
}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'API is running'})

@app.route('/api/strategies', methods=['GET'])
def get_strategies():
    """Get list of available strategies"""
    strategies = [
        {'id': 'momentum', 'name': 'Momentum Strategy'},
        {'id': 'mean_reversion', 'name': 'Mean Reversion Strategy'},
        {'id': 'ma_crossover', 'name': 'Moving Average Crossover'},
        {'id': 'breakout', 'name': 'Breakout Strategy'}
    ]
    return jsonify(strategies)

@app.route('/api/backtest', methods=['POST'])
def run_backtest():
    """Run backtest for a strategy on universe of stocks"""
    try:
        data = request.json
        strategy_id = data.get('strategy', 'momentum')
        universe = data.get('universe', ['AAPL', 'TSLA', 'NVDA'])
        lookback_days = data.get('lookback_days', 180)
        initial_capital = data.get('initial_capital', 10000)

        # Validate strategy
        if strategy_id not in STRATEGIES:
            return jsonify({'error': 'Invalid strategy'}), 400

        # Initialize strategy and risk params
        strategy = STRATEGIES[strategy_id]()
        risk_params = RiskParams()

        # Run backtests
        results = asyncio.run(run_backtests_async(
            strategy, universe, lookback_days, initial_capital, risk_params
        ))

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

async def run_backtests_async(strategy, universe, lookback_days, initial_capital, risk_params):
    """Run backtests asynchronously"""
    results = []

    for symbol in universe:
        try:
            # Get historical data
            historical_data = await getMarketData(symbol, lookback_days)

            if historical_data.empty:
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
            metrics = Metrics(backtest)
            sharpe = metrics.calculatesharperatio()
            drawdown_pct, drawdown_val = metrics.calculatedrawdown()
            ret_val, ret_pct = metrics.calculatetotalreturn()
            win_rate = metrics.calculatewinrate()
            profit_factor = metrics.calculateprofitfactor()

            # Get trades
            buy_trades = [t for t in backtest.trades if t['action'] == 'BUY']
            sell_trades = [t for t in backtest.trades if t['action'] == 'SELL']

            # Format trades for frontend
            trades_formatted = []
            for trade in backtest.trades:
                trades_formatted.append({
                    'symbol': trade['symbol'],
                    'action': trade['action'],
                    'date': trade['date'].isoformat() if hasattr(trade['date'], 'isoformat') else str(trade['date']),
                    'price': float(trade['price']),
                    'shares': float(trade['shares']),
                    'value': float(trade['value']),
                    'reason': trade['reason'],
                    'type': trade['type'],
                    'pnl': float(trade['pnl']) if trade['pnl'] is not None else None
                })

            # Format portfolio history for charts
            portfolio_history_formatted = []
            for entry in backtest.portfolio_history:
                portfolio_history_formatted.append({
                    'date': entry['date'].isoformat() if hasattr(entry['date'], 'isoformat') else str(entry['date']),
                    'total_value': float(entry['total_value']),
                    'cash': float(entry['cash']),
                    'position_value': float(entry['position_value'])
                })

            result = {
                'symbol': symbol,
                'final_value': float(portfolio_value),
                'total_return_pct': float(ret_pct),
                'total_return_val': float(ret_val),
                'sharpe_ratio': float(sharpe) if sharpe != float('inf') else 999,
                'max_drawdown_pct': float(drawdown_pct),
                'max_drawdown_val': float(drawdown_val),
                'win_rate': float(win_rate),
                'profit_factor': float(profit_factor) if profit_factor != float('inf') else 999,
                'buy_trades': len(buy_trades),
                'sell_trades': len(sell_trades),
                'open_positions': len(backtest.positions),
                'trades': trades_formatted,
                'portfolio_history': portfolio_history_formatted
            }
            results.append(result)

        except Exception as e:
            print(f"Error testing {symbol}: {e}")
            continue

    return {
        'strategy': strategy.__class__.__name__,
        'results': results,
        'summary': calculate_summary(results)
    }

def calculate_summary(results):
    """Calculate summary statistics"""
    if not results:
        return {}

    avg_return = sum(r['total_return_pct'] for r in results) / len(results)
    best = max(results, key=lambda x: x['total_return_pct'])
    worst = min(results, key=lambda x: x['total_return_pct'])

    return {
        'avg_return': float(avg_return),
        'best_symbol': best['symbol'],
        'best_return': float(best['total_return_pct']),
        'worst_symbol': worst['symbol'],
        'worst_return': float(worst['total_return_pct']),
        'total_symbols': len(results)
    }

@app.route('/api/compare', methods=['POST'])
def compare_strategies():
    """Compare multiple strategies"""
    try:
        data = request.json
        strategy_ids = data.get('strategies', ['momentum', 'mean_reversion'])
        universe = data.get('universe', ['AAPL'])
        lookback_days = data.get('lookback_days', 180)
        initial_capital = data.get('initial_capital', 10000)

        risk_params = RiskParams()
        all_results = []

        for strategy_id in strategy_ids:
            if strategy_id not in STRATEGIES:
                continue

            strategy = STRATEGIES[strategy_id]()
            results = asyncio.run(run_backtests_async(
                strategy, universe, lookback_days, initial_capital, risk_params
            ))
            all_results.append(results)

        return jsonify({'comparisons': all_results})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
