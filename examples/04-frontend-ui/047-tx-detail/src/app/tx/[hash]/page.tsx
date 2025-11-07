/**
 * Transaction Detail Page
 * Dynamic route: /tx/[hash]
 */

'use client';

import { use, useEffect, useState } from 'react';
import useSWR from 'swr';
import Link from 'next/link';
import {
  getTransaction,
  getTransactionReceipt,
  getLatestBlockNumber,
} from '@/lib/api';
import { Transaction, TransactionReceipt } from '@/types';
import TransactionOverview from '@/components/TransactionOverview';
import InputDataDecoder from '@/components/InputDataDecoder';
import TransactionLogs from '@/components/TransactionLogs';

interface PageProps {
  params: Promise<{
    hash: string;
  }>;
}

export default function TransactionDetailPage({ params }: PageProps) {
  const { hash } = use(params);
  const [confirmations, setConfirmations] = useState<number>(0);

  // Fetch transaction
  const {
    data: transaction,
    error: txError,
    isLoading: txLoading,
  } = useSWR<Transaction>(['transaction', hash], () => getTransaction(hash));

  // Fetch receipt
  const {
    data: receipt,
    error: receiptError,
    isLoading: receiptLoading,
  } = useSWR<TransactionReceipt>(
    transaction ? ['receipt', hash] : null,
    () => getTransactionReceipt(hash)
  );

  // Calculate confirmations
  useEffect(() => {
    if (!transaction) return;

    const updateConfirmations = async () => {
      try {
        const latestBlock = await getLatestBlockNumber();
        const conf = latestBlock - transaction.blockNumber + 1;
        setConfirmations(Math.max(0, conf));
      } catch (error) {
        console.error('Error fetching latest block:', error);
      }
    };

    updateConfirmations();

    // Update every 15 seconds
    const interval = setInterval(updateConfirmations, 15000);
    return () => clearInterval(interval);
  }, [transaction]);

  // Loading state
  if (txLoading || receiptLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="animate-pulse space-y-4">
            <div className="h-8 bg-gray-200 rounded w-1/4"></div>
            <div className="h-64 bg-gray-200 rounded"></div>
            <div className="h-48 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  // Error state
  if (txError || !transaction) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <div className="flex items-start">
              <span className="text-red-600 text-2xl mr-3">⚠️</span>
              <div>
                <h2 className="text-xl font-semibold text-red-900">
                  Transaction Not Found
                </h2>
                <p className="text-red-700 mt-2">
                  Unable to find transaction with hash: <code className="font-mono">{hash}</code>
                </p>
                <p className="text-sm text-red-600 mt-3">
                  Please verify the transaction hash and try again.
                </p>
                <Link
                  href="/"
                  className="inline-block mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
                >
                  ← Back to Home
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center space-x-3">
            <Link
              href="/"
              className="text-blue-600 hover:text-blue-800"
            >
              ← Back
            </Link>
            <h1 className="text-2xl font-bold text-gray-900">
              Transaction Details
            </h1>
          </div>
          <p className="mt-2 text-sm text-gray-600 font-mono break-all">
            {hash}
          </p>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-6">
          {/* Transaction Overview */}
          <TransactionOverview
            transaction={transaction}
            receipt={receipt}
            confirmations={confirmations}
          />

          {/* Input Data */}
          <InputDataDecoder
            input={transaction.input}
            decodedInput={undefined} // TODO: Implement ABI decoding
          />

          {/* Transaction Logs */}
          {receipt && <TransactionLogs logs={receipt.logs} />}

          {/* Raw Data Section (for debugging) */}
          <details className="bg-white shadow rounded-lg overflow-hidden">
            <summary className="px-6 py-4 cursor-pointer hover:bg-gray-50 font-medium text-gray-900">
              🔍 View Raw Transaction Data (Debug)
            </summary>
            <div className="px-6 py-4 border-t border-gray-200">
              <div className="space-y-4">
                <div>
                  <h3 className="text-sm font-medium text-gray-700 mb-2">
                    Transaction Object
                  </h3>
                  <pre className="bg-gray-50 rounded-lg p-4 text-xs font-mono overflow-auto max-h-96">
                    {JSON.stringify(transaction, null, 2)}
                  </pre>
                </div>
                {receipt && (
                  <div>
                    <h3 className="text-sm font-medium text-gray-700 mb-2">
                      Receipt Object
                    </h3>
                    <pre className="bg-gray-50 rounded-lg p-4 text-xs font-mono overflow-auto max-h-96">
                      {JSON.stringify(receipt, null, 2)}
                    </pre>
                  </div>
                )}
              </div>
            </div>
          </details>

          {/* Navigation */}
          <div className="flex items-center justify-between bg-white shadow rounded-lg px-6 py-4">
            <Link
              href={`/block/${transaction.blockNumber}`}
              className="text-blue-600 hover:text-blue-800 hover:underline"
            >
              View Block #{transaction.blockNumber}
            </Link>
            <div className="flex items-center space-x-4">
              <Link
                href={`/address/${transaction.from}`}
                className="text-blue-600 hover:text-blue-800 hover:underline"
              >
                View From Address
              </Link>
              {transaction.to && (
                <Link
                  href={`/address/${transaction.to}`}
                  className="text-blue-600 hover:text-blue-800 hover:underline"
                >
                  View To Address
                </Link>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
