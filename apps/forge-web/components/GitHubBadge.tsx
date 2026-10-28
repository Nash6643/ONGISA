import React from 'react';

export default function GitHubBadge() {
  return (
    <div className="inline-flex items-center space-x-2 px-3 py-1 bg-gray-900 border border-gray-800 rounded-full text-xs font-mono text-gray-300">
      <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
      <span>GitHub Developer Program Integration Active</span>
    </div>
  );
}