/**
 * Transaction Overview Component
 * Displays basic transaction information
 */

'use client';

import Link from 'next/link';
import { Transaction, TransactionReceipt } from '@/types';
import {
  formatAddress,
  formatHash,
  formatNumber,
  formatWei,
  formatGwei,
  formatTimestamp,
  formatTimeAgo,
  copyToClipboard,
  getTransactionType,
} from '@/utils/formatters';
import { useState } from 'react';

interface TransactionOverviewProps {
  transaction: Transaction;
  receipt?: TransactionReceipt;
  confirmations: number;
}

export default function TransactionOverview({
  transaction,
  receipt,
  confirmations,
}: TransactionOverviewProps) {
  const [copied, setCopied] = useState<string | null>(null);

  const handleCopy = async (text: string, field: string) => {
    const success = await copyToClipboard(text);
    if (success) {
      setCopied(field);
      setTimeout(() => setCopied(null), 2000);
    }
  };

  const txType = getTransactionType(transaction);
  const totalFee = receipt
    ? (BigInt(receipt.gasUsed) * BigInt(transaction.gasPrice)).toString()
    : '0';

  return (
    <div className="bg-white shadow rounded-lg overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-xl font-semibold text-gray-900">Transaction Details</h2>
      </div>

      <div className="divide-y divide-gray-200">
        {/* Transaction Hash */}
        <div className="px-6 py-4 sm:grid sm:grid-cols-3 sm:gap-4">
          <dt className="text-sm font-medium text-gray-500">Transaction Hash</dt>
          <dd className="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
            <div className="flex items-center space-x-2">
              <span className="font-mono">{transaction.hash}</span>
              <button
                onClick={() => handleCopy(transaction.hash, 'hash')}
                className="text-blue-600 hover:text-blue-800 text-xs"
              >
                {copied === 'hash' ? '✓ Copied' : '📋 Copy'}
              </button>
            </div>
          </dd>
        </div>

        {/* Status */}
        {receipt && (
          <div className="px-6 py-4 sm:grid sm:grid-cols-3 sm:gap-4">
            <dt className="text-sm font-medium text-gray-500">Status</dt>
            <dd className="mt-1 text-sm sm:col-span-2 sm:mt-0">
              {receipt.status === 1 ? (
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  ✓ Success
                </span>
              ) : (
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                  ✗ Failed
                </span>
              )}
            </dd>
          </div>
        )}

        {/* Block */}
        <div className="px-6 py-4 sm:grid sm:grid-cols-3 sm:gap-4">
          <dt className="text-sm font-medium text-gray-500">Block</dt>
          <dd className="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
            <div className="flex items-center space-x-4">
              <Link
                href={`/block/${transaction.blockNumber}`}
                className="text-blue-600 hover:text-blue-800 hover:underline"
              >
                {formatNumber(transaction.blockNumber)}
              </Link>
              <span className="text-gray-500">
                {confirmations} confirmations
              </span>
            </div>
          </dd>
        </div>

        {/* Timestamp */}
        <div className="px-6 py-4 sm:grid sm:grid-cols-3 sm:gap-4">
          <dt className="text-sm font-medium text-gray-500">Timestamp</dt>
          <dd className="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
            <div className="flex items-center space-x-2">
              <span>⏰ {formatTimestamp(transaction.timestamp)}</span>
              <span className="text-gray-500">({formatTimeAgo(transaction.timestamp)})</span>
            </div>
          </dd>
        </div>

        {/* Transaction Type */}
        <div className="px-6 py-4 sm:grid sm:grid-cols-3 sm:gap-4">
          <dt className="text-sm font-medium text-gray-500">Type</dt>
          <dd className="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium bg-gray-100 text-gray-800">
              {txType}
            </span>
          </dd>
        </div>

        {/* From */}
        <div className="px-6 py-4 sm:grid sm:grid-cols-3 sm:gap-4">
          <dt className="text-sm font-medium text-gray-500">From</dt>
          <dd className="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
            <div className="flex items-center space-x-2">
              <Link
                href={`/address/${transaction.from}`}
                className="text-blue-600 hover:text-blue-800 hover:underline font-mono"
              >
                {transaction.from}
              </Link>
              <button
                onClick={() => handleCopy(transaction.from, 'from')}
                className="text-blue-600 hover:text-blue-800 text-xs"
              >
                {copied === 'from' ? '✓' : '📋'}
              </button>
            </div>
          </dd>
        </div>

        {/* To */}
        <div className="px-6 py-4 sm:grid sm:grid-cols-3 sm:gap-4">
          <dt className="text-sm font-medium text-gray-500">To</dt>
          <dd className="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
            {transaction.to ? (
              <div className="flex items-center space-x-2">
                <Link
                  href={`/address/${transaction.to}`}
                  className="text-blue-600 hover:text-blue-800 hover:underline font-mono"
                >
                  {transaction.to}
                </Link>
                <button
                  onClick={() => handleCopy(transaction.to!, 'to')}
                  className="text-blue-600 hover:text-blue-800 text-xs"
                >
                  {copied === 'to' ? '✓' : '📋'}
                </button>
              </div>
            ) : (
              <span className="text-gray-500 italic">Contract Creation</span>
            )}
          </dd>
        </div>

        {/* Contract Address */}
        {receipt?.contractAddress && (
          <div className="px-6 py-4 sm:grid sm:grid-cols-3 sm:gap-4">
            <dt className="text-sm font-medium text-gray-500">Contract Address</dt>
            <dd className="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
              <div className="flex items-center space-x-2">
                <Link
                  href={`/address/${receipt.contractAddress}`}
                  className="text-blue-600 hover:text-blue-800 hover:underline font-mono"
                >
                  {receipt.contractAddress}
                </Link>
                <button
                  onClick={() => handleCopy(receipt.contractAddress!, 'contract')}
                  className="text-blue-600 hover:text-blue-800 text-xs"
                >
                  {copied === 'contract' ? '✓' : '📋'}
                </button>
              </div>
            </dd>
          </div>
        )}

        {/* Value */}
        <div className="px-6 py-4 sm:grid sm:grid-cols-3 sm:gap-4">
          <dt className="text-sm font-medium text-gray-500">Value</dt>
          <dd className="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
            <span className="font-semibold">{formatWei(transaction.value)} ETH</span>
            <span className="text-gray-500 ml-2 text-xs">
              ({formatNumber(transaction.value)} Wei)
            </span>
          </dd>
        </div>

        {/* Transaction Fee */}
        {receipt && (
          <div className="px-6 py-4 sm:grid sm:grid-cols-3 sm:gap-4">
            <dt className="text-sm font-medium text-gray-500">Transaction Fee</dt>
            <dd className="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
              <span className="font-semibold">{formatWei(totalFee)} ETH</span>
            </dd>
          </div>
        )}

        {/* Gas Price */}
        <div className="px-6 py-4 sm:grid sm:grid-cols-3 sm:gap-4">
          <dt className="text-sm font-medium text-gray-500">Gas Price</dt>
          <dd className="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
            <span>{formatGwei(transaction.gasPrice)} Gwei</span>
            <span className="text-gray-500 ml-2 text-xs">
              ({formatWei(transaction.gasPrice, 9)} ETH)
            </span>
          </dd>
        </div>

        {/* Gas Limit & Usage */}
        <div className="px-6 py-4 sm:grid sm:grid-cols-3 sm:gap-4">
          <dt className="text-sm font-medium text-gray-500">Gas Limit & Usage</dt>
          <dd className="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
            {receipt ? (
              <div className="space-y-1">
                <div>
                  <span className="font-medium">{formatNumber(receipt.gasUsed)}</span>
                  <span className="text-gray-500"> / {formatNumber(transaction.gas)}</span>
                  <span className="ml-2 text-xs text-gray-500">
                    ({((receipt.gasUsed / transaction.gas) * 100).toFixed(2)}% used)
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full"
                    style={{ width: `${(receipt.gasUsed / transaction.gas) * 100}%` }}
                  />
                </div>
              </div>
            ) : (
              <span>{formatNumber(transaction.gas)}</span>
            )}
          </dd>
        </div>

        {/* Nonce */}
        <div className="px-6 py-4 sm:grid sm:grid-cols-3 sm:gap-4">
          <dt className="text-sm font-medium text-gray-500">Nonce</dt>
          <dd className="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
            {transaction.nonce}
          </dd>
        </div>

        {/* Position in Block */}
        <div className="px-6 py-4 sm:grid sm:grid-cols-3 sm:gap-4">
          <dt className="text-sm font-medium text-gray-500">Position in Block</dt>
          <dd className="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
            {transaction.transactionIndex}
          </dd>
        </div>
      </div>
    </div>
  );
}
