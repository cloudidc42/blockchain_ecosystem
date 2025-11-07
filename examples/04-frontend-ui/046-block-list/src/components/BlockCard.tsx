/**
 * BlockCard Component - Display block information
 */
import Link from 'next/link';
import { Clock, Layers, Zap } from 'lucide-react';
import type { Block } from '@/types';
import { formatAddress, formatNumber, formatTimeAgo } from '@/lib/api';

interface BlockCardProps {
  block: Block;
}

export default function BlockCard({ block }: BlockCardProps) {
  const gasUsedPercent = (block.gasUsed / block.gasLimit) * 100;

  return (
    <Link
      href={`/block/${block.number}`}
      className="block p-6 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-50 transition-colors"
    >
      <div className="flex justify-between items-start mb-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Layers className="w-5 h-5 text-primary-500" />
            <h3 className="text-lg font-semibold text-gray-900">
              Block #{formatNumber(block.number)}
            </h3>
          </div>
          <p className="text-sm text-gray-500 flex items-center gap-1">
            <Clock className="w-4 h-4" />
            {formatTimeAgo(block.timestamp)}
          </p>
        </div>
        <span className="px-3 py-1 bg-green-100 text-green-800 text-sm font-medium rounded-full">
          {block.transactionCount} txns
        </span>
      </div>

      <div className="grid grid-cols-2 gap-4 text-sm">
        <div>
          <p className="text-gray-500 mb-1">Miner</p>
          <p className="font-mono text-gray-900">{formatAddress(block.miner)}</p>
        </div>
        <div>
          <p className="text-gray-500 mb-1">Gas Used</p>
          <div className="flex items-center gap-2">
            <Zap className="w-4 h-4 text-yellow-500" />
            <span className="font-medium text-gray-900">
              {gasUsedPercent.toFixed(1)}%
            </span>
          </div>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t border-gray-200">
        <div className="flex justify-between text-xs text-gray-500">
          <span>Hash: {formatAddress(block.hash, 8)}</span>
          <span>Size: {formatNumber(block.size)} bytes</span>
        </div>
      </div>
    </Link>
  );
}
