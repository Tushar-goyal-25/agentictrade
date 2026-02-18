'use client';

import MetricsCard from './MetricsCard';
import PerformanceChart from './PerformanceChart';

interface ResultsDisplayProps {
  results: any;
}

export default function ResultsDisplay({ results }: ResultsDisplayProps) {
  if (!results || !results.results) {
    return null;
  }

  const { strategy, results: stockResults, summary } = results;

  // Sort by return
  const sortedResults = [...stockResults].sort(
    (a, b) => b.total_return_pct - a.total_return_pct
  );

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          {strategy} Results
        </h2>

        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="bg-blue-50 rounded-lg p-4">
            <p className="text-sm text-gray-600">Average Return</p>
            <p className={`text-2xl font-bold ${summary.avg_return >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {summary.avg_return?.toFixed(2)}%
            </p>
          </div>
          <div className="bg-green-50 rounded-lg p-4">
            <p className="text-sm text-gray-600">Best Performer</p>
            <p className="text-xl font-bold text-gray-900">{summary.best_symbol}</p>
            <p className="text-sm text-green-600">+{summary.best_return?.toFixed(2)}%</p>
          </div>
          <div className="bg-red-50 rounded-lg p-4">
            <p className="text-sm text-gray-600">Worst Performer</p>
            <p className="text-xl font-bold text-gray-900">{summary.worst_symbol}</p>
            <p className="text-sm text-red-600">{summary.worst_return?.toFixed(2)}%</p>
          </div>
        </div>

        {/* Top 3 Strategies */}
        <div className="mb-6">
          <h3 className="text-lg font-bold text-gray-900 mb-3">🏆 Top 3 Recommendations</h3>
          <div className="grid grid-cols-3 gap-4">
            {sortedResults.slice(0, 3).map((result, index) => (
              <div key={result.symbol} className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-lg p-4 border-2 border-yellow-300">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-2xl font-bold text-gray-900">{result.symbol}</span>
                  <span className="text-2xl">{index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉'}</span>
                </div>
                <p className={`text-xl font-bold ${result.total_return_pct >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {result.total_return_pct >= 0 ? '+' : ''}{result.total_return_pct.toFixed(2)}%
                </p>
                <div className="mt-2 text-xs text-gray-600 space-y-1">
                  <p>Sharpe: {result.sharpe_ratio.toFixed(2)}</p>
                  <p>Win Rate: {result.win_rate.toFixed(0)}%</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Individual Stock Results */}
      {sortedResults.map((result) => (
        <div key={result.symbol} className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-gray-900">{result.symbol}</h3>
            <span className={`text-2xl font-bold ${result.total_return_pct >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {result.total_return_pct >= 0 ? '+' : ''}{result.total_return_pct.toFixed(2)}%
            </span>
          </div>

          {/* Metrics Grid */}
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
            <MetricsCard
              label="Final Value"
              value={`$${result.final_value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
            />
            <MetricsCard
              label="Sharpe Ratio"
              value={result.sharpe_ratio === 999 ? '∞' : result.sharpe_ratio.toFixed(2)}
            />
            <MetricsCard
              label="Max Drawdown"
              value={`${result.max_drawdown_pct.toFixed(2)}%`}
              negative
            />
            <MetricsCard
              label="Win Rate"
              value={`${result.win_rate.toFixed(1)}%`}
            />
            <MetricsCard
              label="Profit Factor"
              value={result.profit_factor === 999 ? '∞' : result.profit_factor.toFixed(2)}
            />
          </div>

          {/* Portfolio Chart */}
          {result.portfolio_history && result.portfolio_history.length > 0 && (
            <PerformanceChart data={result.portfolio_history} symbol={result.symbol} />
          )}

          {/* Trade Stats */}
          <div className="mt-4 flex gap-4 text-sm text-gray-600">
            <span>📈 {result.buy_trades} BUY trades</span>
            <span>📉 {result.sell_trades} SELL trades</span>
            <span>💼 {result.open_positions} open positions</span>
          </div>
        </div>
      ))}
    </div>
  );
}
