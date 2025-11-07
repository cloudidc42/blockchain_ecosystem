'use client';

/**
 * Block Detail Page
 */
import { use } from 'react';
import Link from 'next/link';
import useSWR from 'swr';
import { ArrowLeft, Hash, Clock, User, Zap, Database } from 'lucide-react';
import Loading from '@/components/Loading';
import ErrorMessage from '@/components/ErrorMessage';
import {
  getBlockByNumber,
  formatNumber,
  formatTimestamp,
  formatAddress,
  formatHash,
} from '@/lib/api';
import type { Block } from '@/types';

export default function BlockDetailPage({
  params,
}: {
  params: Promise<{ number: string }>;
}) {
  const { number } = use(params);
  const blockNumber = parseInt(number);

  const { data: block, error, isLoading } = useSWR<Block>(
    ['block', blockNumber],
    () => getBlockByNumber(blockNumber, true)
  );

  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Loading message="Loading block details..." />
      </div>
    );
  }

  if (error || !block) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <ErrorMessage message="Block not found or failed to load" />
      </div>
    );
  }

  const gasUsedPercent = (block.gasUsed / block.gasLimit) * 100;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back Button */}
      <Link
        href="/"
        className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 mb-6 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Blocks
      </Link>

      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Block #{formatNumber(block.number)}
        </h1>
        <p className="text-gray-600">
          {formatTimestamp(block.timestamp)}
        </p>
      </div>

      {/* Main Info Card */}
      <div className="bg-white rounded-lg shadow border border-gray-200 p-6 mb-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">
          Block Information
        </h2>

        <div className="space-y-4">
          {/* Hash */}
          <div className="flex flex-col sm:flex-row sm:items-center py-3 border-b border-gray-200">
            <div className="flex items-center gap-2 sm:w-48 mb-2 sm:mb-0">
              <Hash className="w-4 h-4 text-gray-400" />
              <span className="text-sm font-medium text-gray-600">Hash</span>
            </div>
            <span className="font-mono text-sm text-gray-900 break-all">
              {block.hash}
            </span>
          </div>

          {/* Parent Hash */}
          <div className="flex flex-col sm:flex-row sm:items-center py-3 border-b border-gray-200">
            <div className="flex items-center gap-2 sm:w-48 mb-2 sm:mb-0">
              <Hash className="w-4 h-4 text-gray-400" />
              <span className="text-sm font-medium text-gray-600">Parent Hash</span>
            </div>
            <Link
              href={`/block/${block.number - 1}`}
              className="font-mono text-sm text-primary-600 hover:text-primary-700 break-all"
            >
              {block.parentHash}
            </Link>
          </div>

          {/* Timestamp */}
          <div className="flex flex-col sm:flex-row sm:items-center py-3 border-b border-gray-200">
            <div className="flex items-center gap-2 sm:w-48 mb-2 sm:mb-0">
              <Clock className="w-4 h-4 text-gray-400" />
              <span className="text-sm font-medium text-gray-600">Timestamp</span>
            </div>
            <span className="text-sm text-gray-900">
              {formatTimestamp(block.timestamp)} ({block.timestamp})
            </span>
          </div>

          {/* Miner */}
          <div className="flex flex-col sm:flex-row sm:items-center py-3 border-b border-gray-200">
            <div className="flex items-center gap-2 sm:w-48 mb-2 sm:mb-0">
              <User className="w-4 h-4 text-gray-400" />
              <span className="text-sm font-medium text-gray-600">Miner</span>
            </div>
            <span className="font-mono text-sm text-gray-900 break-all">
              {block.miner}
            </span>
          </div>

          {/* Gas Usage */}
          <div className="flex flex-col sm:flex-row sm:items-center py-3 border-b border-gray-200">
            <div className="flex items-center gap-2 sm:w-48 mb-2 sm:mb-0">
              <Zap className="w-4 h-4 text-gray-400" />
              <span className="text-sm font-medium text-gray-600">Gas Used</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-sm text-gray-900">
                {formatNumber(block.gasUsed)} / {formatNumber(block.gasLimit)}
              </span>
              <span className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs font-medium rounded">
                {gasUsedPercent.toFixed(2)}%
              </span>
            </div>
          </div>

          {/* Difficulty */}
          <div className="flex flex-col sm:flex-row sm:items-center py-3 border-b border-gray-200">
            <div className="flex items-center gap-2 sm:w-48 mb-2 sm:mb-0">
              <Database className="w-4 h-4 text-gray-400" />
              <span className="text-sm font-medium text-gray-600">Difficulty</span>
            </div>
            <span className="text-sm text-gray-900">
              {formatNumber(block.difficulty)}
            </span>
          </div>

          {/* Size */}
          <div className="flex flex-col sm:flex-row sm:items-center py-3">
            <div className="flex items-center gap-2 sm:w-48 mb-2 sm:mb-0">
              <Database className="w-4 h-4 text-gray-400" />
              <span className="text-sm font-medium text-gray-600">Size</span>
            </div>
            <span className="text-sm text-gray-900">
              {formatNumber(block.size)} bytes
            </span>
          </div>
        </div>
      </div>

      {/* Transactions */}
      <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-gray-900">
            Transactions
          </h2>
          <span className="px-3 py-1 bg-green-100 text-green-800 text-sm font-medium rounded-full">
            {block.transactionCount} transactions
          </span>
        </div>

        {block.transactions && block.transactions.length > 0 ? (
          <div className="space-y-2">
            {block.transactions.slice(0, 10).map((txHash, index) => (
              <div
                key={txHash}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <span className="text-sm text-gray-500">#{index}</span>
                  <span className="font-mono text-sm text-gray-900">
                    {formatHash(txHash, 16)}
                  </span>
                </div>
              </div>
            ))}
            {block.transactions.length > 10 && (
              <p className="text-center text-sm text-gray-500 pt-4">
                ... and {block.transactions.length - 10} more transactions
              </p>
            )}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            No transactions in this block
          </div>
        )}
      </div>

      {/* Navigation */}
      <div className="flex justify-between mt-8">
        {block.number > 0 ? (
          <Link
            href={`/block/${block.number - 1}`}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            ← Previous Block
          </Link>
        ) : (
          <div />
        )}
        <Link
          href={`/block/${block.number + 1}`}
          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
        >
          Next Block →
        </Link>
      </div>
    </div>
  );
}
