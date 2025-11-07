/**
 * StatsCard Component - Display statistics
 */
import { LucideIcon } from 'lucide-react';

interface StatsCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  subtitle?: string;
  trend?: 'up' | 'down' | 'neutral';
}

export default function StatsCard({
  title,
  value,
  icon: Icon,
  subtitle,
  trend = 'neutral',
}: StatsCardProps) {
  const trendColors = {
    up: 'text-green-600',
    down: 'text-red-600',
    neutral: 'text-gray-600',
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-medium text-gray-500">{title}</h3>
        <Icon className="w-5 h-5 text-primary-500" />
      </div>
      <p className="text-2xl font-bold text-gray-900 mb-1">{value}</p>
      {subtitle && (
        <p className={`text-sm ${trendColors[trend]}`}>{subtitle}</p>
      )}
    </div>
  );
}
