import React from 'react';

interface MetricsCardProps {
  title: string;
  value: string | number;
  badge?: string;
}

export default function MetricsCard({ title, value, badge }: MetricsCardProps) {
  return (
    <div className="bg-gray-900 border border-gray-800 p-5 rounded-2xl shadow-xl flex flex-col justify-between">
      <div className="flex items-center justify-between">
        <span className="text-xs font-mono text-gray-400 uppercase tracking-wider">{title}</span>
        {badge && <span className="text-[10px] font-mono px-2 py-0.5 bg-blue-950 text-blue-400 border border-blue-900 rounded">{badge}</span>}
      </div>
      <div className="text-2xl font-bold text-white mt-3 font-mono">{value}</div>
    </div>
  );
}