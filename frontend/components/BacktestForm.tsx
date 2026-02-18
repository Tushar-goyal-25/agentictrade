'use client';

import { useState } from 'react';

interface BacktestFormProps {
  onSubmit: (results: any) => void;
  loading: boolean;
  setLoading: (loading: boolean) => void;
}

const STRATEGIES = [
  { id: 'momentum', name: 'Momentum Strategy' },
  { id: 'mean_reversion', name: 'Mean Reversion' },
  { id: 'ma_crossover', name: 'MA Crossover' },
  { id: 'breakout', name: 'Breakout' },
];

const POPULAR_STOCKS = [
  'AAPL', 'TSLA', 'NVDA', 'AMD', 'META', 'GOOGL', 'MSFT',
  'AMZN', 'COIN', 'PLTR', 'SHOP', 'RIOT'
];

export default function BacktestForm({ onSubmit, loading, setLoading }: BacktestFormProps) {
  const [strategy, setStrategy] = useState('momentum');
  const [selectedStocks, setSelectedStocks] = useState(['AAPL', 'TSLA', 'NVDA']);
  const [customStock, setCustomStock] = useState('');
  const [capital, setCapital] = useState('10000');
  const [lookbackDays, setLookbackDays] = useState('180');

  const toggleStock = (stock: string) => {
    if (selectedStocks.includes(stock)) {
      setSelectedStocks(selectedStocks.filter(s => s !== stock));
    } else {
      setSelectedStocks([...selectedStocks, stock]);
    }
  };

  const addCustomStock = () => {
    const stock = customStock.toUpperCase().trim();
    if (stock && !selectedStocks.includes(stock)) {
      setSelectedStocks([...selectedStocks, stock]);
      setCustomStock('');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('http://localhost:5001/api/backtest', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          strategy,
          universe: selectedStocks,
          initial_capital: parseFloat(capital),
          lookback_days: parseInt(lookbackDays),
        }),
      });

      const data = await response.json();
      onSubmit(data);
    } catch (error) {
      console.error('Error running backtest:', error);
      alert('Failed to run backtest. Make sure the API is running on port 5000.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Configure Backtest</h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Strategy Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Strategy
          </label>
          <select
            value={strategy}
            onChange={(e) => setStrategy(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {STRATEGIES.map(s => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </select>
        </div>

        {/* Stock Universe */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Stock Universe ({selectedStocks.length} selected)
          </label>
          <div className="grid grid-cols-3 gap-2 mb-3">
            {POPULAR_STOCKS.map(stock => (
              <button
                key={stock}
                type="button"
                onClick={() => toggleStock(stock)}
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  selectedStocks.includes(stock)
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {stock}
              </button>
            ))}
          </div>
          <div className="flex gap-2">
            <input
              type="text"
              value={customStock}
              onChange={(e) => setCustomStock(e.target.value)}
              placeholder="Add custom (e.g., NFLX)"
              className="flex-1 border border-gray-300 rounded-lg px-4 py-2 text-sm focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="button"
              onClick={addCustomStock}
              className="px-4 py-2 bg-gray-800 text-white rounded-lg text-sm hover:bg-gray-700"
            >
              Add
            </button>
          </div>
        </div>

        {/* Initial Capital */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Initial Capital ($)
          </label>
          <input
            type="number"
            value={capital}
            onChange={(e) => setCapital(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
            min="1000"
            step="1000"
          />
        </div>

        {/* Lookback Period */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Lookback Period (days)
          </label>
          <input
            type="number"
            value={lookbackDays}
            onChange={(e) => setLookbackDays(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
            min="30"
            max="365"
            step="30"
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading || selectedStocks.length === 0}
          className="w-full bg-blue-600 text-white font-medium py-3 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Running Backtest...' : 'Run Backtest'}
        </button>
      </form>
    </div>
  );
}
