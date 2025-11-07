/**
 * Home Page
 * Landing page with transaction hash search
 */

'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function HomePage() {
  const router = useRouter();
  const [txHash, setTxHash] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Basic validation
    if (!txHash) {
      setError('Please enter a transaction hash');
      return;
    }

    // Check if it looks like a valid hash (0x + 64 hex characters)
    if (!/^0x[a-fA-F0-9]{64}$/.test(txHash)) {
      setError('Invalid transaction hash format. Should be 0x followed by 64 hex characters');
      return;
    }

    // Navigate to transaction detail page
    router.push(`/tx/${txHash}`);
  };

  // Example transaction hashes (you can update these with real ones)
  const exampleHashes = [
    '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef',
    '0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🔍 Transaction Detail Explorer
          </h1>
          <p className="text-lg text-gray-600">
            Search and view detailed information about any blockchain transaction
          </p>
        </div>

        {/* Search Form */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <form onSubmit={handleSubmit}>
            <label htmlFor="txHash" className="block text-sm font-medium text-gray-700 mb-2">
              Transaction Hash
            </label>
            <div className="flex space-x-4">
              <input
                type="text"
                id="txHash"
                value={txHash}
                onChange={(e) => setTxHash(e.target.value)}
                placeholder="0x..."
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
              />
              <button
                type="submit"
                className="px-8 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                Search
              </button>
            </div>
            {error && (
              <p className="mt-2 text-sm text-red-600">
                {error}
              </p>
            )}
          </form>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-3xl mb-3">📊</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Complete Details
            </h3>
            <p className="text-sm text-gray-600">
              View all transaction information including status, gas usage, and value transferred
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-3xl mb-3">📝</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Input Data Decoder
            </h3>
            <p className="text-sm text-gray-600">
              Decode transaction input data and view function calls and parameters
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-3xl mb-3">📋</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Event Logs
            </h3>
            <p className="text-sm text-gray-600">
              Explore emitted events and logs from smart contract interactions
            </p>
          </div>
        </div>

        {/* Example Section */}
        <div className="bg-blue-50 rounded-lg border border-blue-200 p-6">
          <h3 className="text-sm font-medium text-blue-900 mb-3">
            💡 Example Transaction Hashes (for testing)
          </h3>
          <div className="space-y-2">
            {exampleHashes.map((hash, index) => (
              <button
                key={index}
                onClick={() => setTxHash(hash)}
                className="block w-full text-left px-4 py-2 bg-white rounded border border-blue-200 hover:border-blue-400 hover:bg-blue-50 transition-colors"
              >
                <code className="text-xs text-blue-600 break-all">{hash}</code>
              </button>
            ))}
          </div>
          <p className="text-xs text-blue-700 mt-3">
            Click on an example hash to populate the search field
          </p>
        </div>

        {/* Information */}
        <div className="mt-12 text-center text-sm text-gray-500">
          <p>
            This page allows you to view detailed information about any transaction on the blockchain.
          </p>
          <p className="mt-2">
            Connect to your backend API at{' '}
            <code className="bg-gray-100 px-2 py-1 rounded">
              {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}
            </code>
          </p>
        </div>
      </div>
    </div>
  );
}
