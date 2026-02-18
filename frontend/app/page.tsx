'use client';

import { useState } from 'react';
import BacktestForm from '@/components/BacktestForm';
import ResultsDisplay from '@/components/ResultsDisplay';
import Header from '@/components/Header';

export default function Home() {
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <Header />

      <main className="container mx-auto px-4 py-8">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Agentic Trading System
          </h1>
          <p className="text-gray-600">
            Backtest trading strategies and analyze performance metrics
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left sidebar - Form */}
          <div className="lg:col-span-1">
            <BacktestForm
              onSubmit={setResults}
              loading={loading}
              setLoading={setLoading}
            />
          </div>

          {/* Main content - Results */}
          <div className="lg:col-span-2">
            {loading ? (
              <div className="bg-white rounded-lg shadow-lg p-8">
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                  <span className="ml-4 text-gray-600">Running backtest...</span>
                </div>
              </div>
            ) : results ? (
              <ResultsDisplay results={results} />
            ) : (
              <div className="bg-white rounded-lg shadow-lg p-8">
                <div className="text-center text-gray-500">
                  <svg className="mx-auto h-12 w-12 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  <p>Configure and run a backtest to see results</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
