'use client';

/**
 * Statistics Page
 */
import useSWR from 'swr';
import { Activity, Blocks, Clock, TrendingUp, Zap, Fuel } from 'lucide-react';
import StatsCard from '@/components/StatsCard';
import Loading from '@/components/Loading';
import ErrorMessage from '@/components/ErrorMessage';
import { getBlockchainStats, getGasStats, formatNumber, formatGwei } from '@/lib/api';
import type { BlockchainStats, GasStats } from '@/types';

export default function StatsPage() {
  const {
    data: stats,
    error: statsError,
    isLoading: statsLoading,
  } = useSWR<BlockchainStats>('blockchain-stats', getBlockchainStats, {
    refreshInterval: 10000,
  });

  const {
    data: gasStats,
    error: gasError,
    isLoading: gasLoading,
  } = useSWR<GasStats>('gas-stats', getGasStats, {
    refreshInterval: 5000,
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Network Statistics
        </h1>
        <p className="text-gray-600">
          Real-time blockchain network metrics and gas prices
        </p>
      </div>

      {/* Blockchain Stats */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Blockchain Metrics
        </h2>
        {statsLoading ? (
          <Loading message="Loading statistics..." />
        ) : statsError ? (
          <ErrorMessage message="Failed to load blockchain statistics" />
        ) : stats ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <StatsCard
              title="Latest Block"
              value={formatNumber(stats.latest_block)}
              icon={Blocks}
              subtitle="Current block height"
            />
            <StatsCard
              title="Total Transactions"
              value={formatNumber(stats.total_transactions)}
              icon={TrendingUp}
              subtitle="Approximate total"
            />
            <StatsCard
              title="Avg Block Time"
              value={`${stats.avg_block_time.toFixed(2)}s`}
              icon={Clock}
              subtitle="Last 100 blocks"
            />
            <StatsCard
              title="Avg Gas Price"
              value={`${formatGwei(stats.avg_gas_price)} Gwei`}
              icon={Zap}
              subtitle="Network average"
            />
            <StatsCard
              title="Difficulty"
              value={formatNumber(stats.difficulty)}
              icon={Activity}
              subtitle="Current difficulty"
            />
            <StatsCard
              title="Pending Transactions"
              value={formatNumber(stats.pending_transactions)}
              icon={TrendingUp}
              subtitle="In mempool"
            />
          </div>
        ) : null}
      </div>

      {/* Gas Prices */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Gas Price Estimates
        </h2>
        {gasLoading ? (
          <Loading message="Loading gas prices..." />
        ) : gasError ? (
          <ErrorMessage message="Failed to load gas prices" />
        ) : gasStats ? (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
              <StatsCard
                title="Slow"
                value={`${gasStats.slow} Gwei`}
                icon={Fuel}
                subtitle="Low priority"
              />
              <StatsCard
                title="Standard"
                value={`${gasStats.standard} Gwei`}
                icon={Fuel}
                subtitle="Normal priority"
              />
              <StatsCard
                title="Fast"
                value={`${gasStats.fast} Gwei`}
                icon={Fuel}
                subtitle="High priority"
              />
              <StatsCard
                title="Instant"
                value={`${gasStats.instant} Gwei`}
                icon={Fuel}
                subtitle="Maximum priority"
              />
            </div>

            {/* Gas Price Chart (Placeholder) */}
            <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Gas Price Comparison
              </h3>
              <div className="space-y-4">
                {[
                  { label: 'Slow', value: gasStats.slow, color: 'bg-blue-500' },
                  { label: 'Standard', value: gasStats.standard, color: 'bg-green-500' },
                  { label: 'Fast', value: gasStats.fast, color: 'bg-yellow-500' },
                  { label: 'Instant', value: gasStats.instant, color: 'bg-red-500' },
                ].map((item) => {
                  const maxValue = Math.max(
                    gasStats.slow,
                    gasStats.standard,
                    gasStats.fast,
                    gasStats.instant
                  );
                  const percentage = (item.value / maxValue) * 100;

                  return (
                    <div key={item.label} className="flex items-center gap-4">
                      <div className="w-24 text-sm font-medium text-gray-700">
                        {item.label}
                      </div>
                      <div className="flex-1">
                        <div className="w-full bg-gray-200 rounded-full h-8 relative">
                          <div
                            className={`${item.color} h-8 rounded-full flex items-center justify-end px-3 transition-all duration-500`}
                            style={{ width: `${percentage}%` }}
                          >
                            <span className="text-white text-sm font-semibold">
                              {item.value} Gwei
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </>
        ) : null}
      </div>

      {/* Auto-refresh indicator */}
      <div className="mt-8 text-center text-sm text-gray-500">
        Auto-refreshing • Stats: 10s • Gas: 5s
      </div>
    </div>
  );
}
