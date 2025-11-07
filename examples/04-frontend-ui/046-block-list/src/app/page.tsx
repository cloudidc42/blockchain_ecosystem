'use client';

/**
 * Home Page - Block List
 */
import { useState, useEffect } from 'react';
import useSWR from 'swr';
import { Blocks, TrendingUp, Clock, Zap } from 'lucide-react';
import BlockCard from '@/components/BlockCard';
import StatsCard from '@/components/StatsCard';
import Pagination from '@/components/Pagination';
import Loading from '@/components/Loading';
import ErrorMessage from '@/components/ErrorMessage';
import { getBlocks, getBlockchainStats, formatNumber, formatGwei } from '@/lib/api';
import type { BlockList, BlockchainStats } from '@/types';

export default function Home() {
  const [page, setPage] = useState(1);
  const pageSize = 20;

  // Fetch blocks
  const {
    data: blockList,
    error: blocksError,
    isLoading: blocksLoading,
    mutate: refetchBlocks,
  } = useSWR<BlockList>(
    ['blocks', page, pageSize],
    () => getBlocks(page, pageSize),
    {
      refreshInterval: 12000, // Auto-refresh every 12 seconds
      revalidateOnFocus: false,
    }
  );

  // Fetch stats
  const {
    data: stats,
    error: statsError,
    isLoading: statsLoading,
  } = useSWR<BlockchainStats>('stats', getBlockchainStats, {
    refreshInterval: 10000, // Refresh every 10 seconds
    revalidateOnFocus: false,
  });

  // Scroll to top on page change
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [page]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Latest Blocks
        </h1>
        <p className="text-gray-600">
          Real-time blockchain data and statistics
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statsLoading ? (
          <>
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-32 bg-gray-200 animate-pulse rounded-lg" />
            ))}
          </>
        ) : statsError ? (
          <div className="col-span-4">
            <ErrorMessage message="Failed to load statistics" />
          </div>
        ) : stats ? (
          <>
            <StatsCard
              title="Latest Block"
              value={formatNumber(stats.latest_block)}
              icon={Blocks}
              subtitle="Block height"
            />
            <StatsCard
              title="Total Transactions"
              value={formatNumber(stats.total_transactions)}
              icon={TrendingUp}
              subtitle="Approximate"
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
              subtitle="Current average"
            />
          </>
        ) : null}
      </div>

      {/* Blocks List */}
      <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-gray-900">
            Recent Blocks
          </h2>
          {blockList && (
            <span className="text-sm text-gray-500">
              Page {blockList.page} • {blockList.blocks.length} blocks
            </span>
          )}
        </div>

        {blocksLoading ? (
          <Loading message="Loading blocks..." />
        ) : blocksError ? (
          <ErrorMessage
            message="Failed to load blocks. Please check if the API is running."
            retry={() => refetchBlocks()}
          />
        ) : blockList && blockList.blocks.length > 0 ? (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              {blockList.blocks.map((block) => (
                <BlockCard key={block.number} block={block} />
              ))}
            </div>

            <Pagination
              currentPage={blockList.page}
              hasNext={blockList.has_next}
              hasPrev={blockList.has_prev}
              onPageChange={setPage}
            />
          </>
        ) : (
          <div className="text-center py-12 text-gray-500">
            No blocks found
          </div>
        )}
      </div>

      {/* Connection Status */}
      <div className="mt-6 text-center text-sm text-gray-500">
        {blockList ? (
          <p>
            Connected to blockchain • Auto-refreshing every 12 seconds
          </p>
        ) : (
          <p>Connecting to blockchain...</p>
        )}
      </div>
    </div>
  );
}
