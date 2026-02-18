'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface PerformanceChartProps {
  data: Array<{
    date: string;
    total_value: number;
    cash: number;
    position_value: number;
  }>;
  symbol: string;
}

export default function PerformanceChart({ data, symbol }: PerformanceChartProps) {
  // Format data for chart
  const chartData = data.map((entry, index) => ({
    index,
    value: entry.total_value,
    date: new Date(entry.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  }));

  const minValue = Math.min(...chartData.map(d => d.value));
  const maxValue = Math.max(...chartData.map(d => d.value));
  const initialValue = chartData[0]?.value || 10000;
  const finalValue = chartData[chartData.length - 1]?.value || initialValue;
  const isProfit = finalValue >= initialValue;

  return (
    <div className="mt-4">
      <h4 className="text-sm font-medium text-gray-700 mb-3">Portfolio Value Over Time</h4>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 11, fill: '#6b7280' }}
            interval={Math.floor(chartData.length / 6)}
          />
          <YAxis
            domain={[Math.floor(minValue * 0.99), Math.ceil(maxValue * 1.01)]}
            tick={{ fontSize: 11, fill: '#6b7280' }}
            tickFormatter={(value) => `$${value.toLocaleString()}`}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              fontSize: '12px'
            }}
            formatter={(value: number) => [`$${value.toFixed(2)}`, 'Portfolio Value']}
          />
          <Line
            type="monotone"
            dataKey="value"
            stroke={isProfit ? '#10b981' : '#ef4444'}
            strokeWidth={2}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
