/**
 * Transaction Logs Component
 * Displays event logs from transaction receipt
 */

'use client';

import { useState } from 'react';
import { TransactionLog } from '@/types';
import { formatAddress, copyToClipboard } from '@/utils/formatters';
import Link from 'next/link';

interface TransactionLogsProps {
  logs: TransactionLog[];
}

export default function TransactionLogs({ logs }: TransactionLogsProps) {
  const [expandedLogs, setExpandedLogs] = useState<Set<number>>(new Set());
  const [copiedField, setCopiedField] = useState<string | null>(null);

  if (!logs || logs.length === 0) {
    return (
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">Logs</h2>
        </div>
        <div className="px-6 py-4">
          <p className="text-sm text-gray-500 italic">No logs emitted</p>
        </div>
      </div>
    );
  }

  const toggleLog = (index: number) => {
    const newExpanded = new Set(expandedLogs);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedLogs(newExpanded);
  };

  const handleCopy = async (text: string, field: string) => {
    const success = await copyToClipboard(text);
    if (success) {
      setCopiedField(field);
      setTimeout(() => setCopiedField(null), 2000);
    }
  };

  return (
    <div className="bg-white shadow rounded-lg overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-xl font-semibold text-gray-900">
          Logs <span className="text-gray-500 font-normal">({logs.length})</span>
        </h2>
      </div>

      <div className="divide-y divide-gray-200">
        {logs.map((log, index) => {
          const isExpanded = expandedLogs.has(index);

          return (
            <div key={index} className="px-6 py-4">
              {/* Log Header */}
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      Log #{log.logIndex}
                    </span>
                    <Link
                      href={`/address/${log.address}`}
                      className="text-sm text-blue-600 hover:text-blue-800 hover:underline font-mono"
                    >
                      {formatAddress(log.address, 8, 6)}
                    </Link>
                  </div>

                  {/* Topics Preview */}
                  <div className="mt-2 text-sm text-gray-600">
                    <span className="font-medium">{log.topics.length} Topics</span>
                    {log.data && log.data !== '0x' && (
                      <span className="ml-2">• Data present</span>
                    )}
                  </div>
                </div>

                <button
                  onClick={() => toggleLog(index)}
                  className="ml-4 text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  {isExpanded ? '▼ Collapse' : '▶ Expand'}
                </button>
              </div>

              {/* Expanded Log Details */}
              {isExpanded && (
                <div className="mt-4 space-y-4">
                  {/* Address */}
                  <div>
                    <div className="text-xs font-medium text-gray-500 mb-1">
                      Contract Address:
                    </div>
                    <div className="flex items-center space-x-2">
                      <Link
                        href={`/address/${log.address}`}
                        className="text-sm text-blue-600 hover:text-blue-800 hover:underline font-mono"
                      >
                        {log.address}
                      </Link>
                      <button
                        onClick={() => handleCopy(log.address, `address-${index}`)}
                        className="text-blue-600 hover:text-blue-800 text-xs"
                      >
                        {copiedField === `address-${index}` ? '✓' : '📋'}
                      </button>
                    </div>
                  </div>

                  {/* Topics */}
                  <div>
                    <div className="text-xs font-medium text-gray-500 mb-2">
                      Topics:
                    </div>
                    <div className="space-y-2">
                      {log.topics.map((topic, topicIndex) => (
                        <div
                          key={topicIndex}
                          className="bg-gray-50 rounded-lg p-3"
                        >
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-xs text-gray-500">
                              [{topicIndex}]{topicIndex === 0 ? ' Event Signature' : ''}
                            </span>
                            <button
                              onClick={() =>
                                handleCopy(topic, `topic-${index}-${topicIndex}`)
                              }
                              className="text-blue-600 hover:text-blue-800 text-xs"
                            >
                              {copiedField === `topic-${index}-${topicIndex}`
                                ? '✓'
                                : '📋'}
                            </button>
                          </div>
                          <code className="text-xs font-mono text-gray-900 break-all">
                            {topic}
                          </code>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Data */}
                  {log.data && log.data !== '0x' && (
                    <div>
                      <div className="text-xs font-medium text-gray-500 mb-1">
                        Data:
                      </div>
                      <div className="bg-gray-50 rounded-lg p-3">
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs text-gray-500">
                            Hex ({new Blob([log.data]).size} bytes)
                          </span>
                          <button
                            onClick={() => handleCopy(log.data, `data-${index}`)}
                            className="text-blue-600 hover:text-blue-800 text-xs"
                          >
                            {copiedField === `data-${index}` ? '✓' : '📋'}
                          </button>
                        </div>
                        <pre className="text-xs font-mono text-gray-900 whitespace-pre-wrap break-all">
                          {log.data}
                        </pre>
                      </div>
                    </div>
                  )}

                  {/* Additional Info */}
                  <div className="grid grid-cols-2 gap-4 text-xs">
                    <div>
                      <span className="text-gray-500">Block Number:</span>
                      <span className="ml-2 font-mono">{log.blockNumber}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Transaction Index:</span>
                      <span className="ml-2 font-mono">{log.transactionIndex}</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Summary */}
      <div className="px-6 py-3 bg-gray-50 border-t border-gray-200">
        <p className="text-xs text-gray-600">
          Click "Expand" on any log to view full details including topics and data
        </p>
      </div>
    </div>
  );
}
