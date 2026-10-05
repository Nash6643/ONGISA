'use client';

import React from 'react';

interface DiffViewerProps {
  originalCode: string;
  refactoredCode: string;
  filePath?: string;
}

export default function DiffViewer({ originalCode, refactoredCode, filePath }: DiffViewerProps) {
  const originalLines = originalCode ? originalCode.split('\n') : [];
  const refactoredLines = refactoredCode ? refactoredCode.split('\n') : [];

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden shadow-2xl">
      <div className="bg-gray-950 px-4 py-3 border-b border-gray-800 flex items-center justify-between">
        <span className="text-sm font-mono text-gray-400">{filePath || 'code_diff.ts'}</span>
        <div className="flex items-center space-x-2 text-xs font-mono">
          <span className="px-2 py-1 bg-red-950/50 text-red-400 border border-red-900/50 rounded">Original</span>
          <span className="px-2 py-1 bg-emerald-950/50 text-emerald-400 border border-emerald-900/50 rounded">Refactored</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-gray-800 text-xs font-mono overflow-x-auto">
        {/* Original Code View */}
        <div className="p-4 bg-gray-900/50">
          <div className="text-gray-500 mb-2 font-semibold uppercase tracking-wider">Before</div>
          <pre className="text-gray-300 space-y-1">
            {originalLines.map((line, idx) => (
              <div key={idx} className="flex">
                <span className="w-8 text-gray-600 select-none text-right pr-3">{idx + 1}</span>
                <span className="flex-1 text-red-300/90 bg-red-950/10 px-1 rounded">{line || ' '}</span>
              </div>
            ))}
          </pre>
        </div>

        {/* Refactored Code View */}
        <div className="p-4 bg-gray-900/50">
          <div className="text-gray-500 mb-2 font-semibold uppercase tracking-wider">After (AI Suggested)</div>
          <pre className="text-gray-300 space-y-1">
            {refactoredLines.map((line, idx) => (
              <div key={idx} className="flex">
                <span className="w-8 text-gray-600 select-none text-right pr-3">{idx + 1}</span>
                <span className="flex-1 text-emerald-300/90 bg-emerald-950/10 px-1 rounded">{line || ' '}</span>
              </div>
            ))}
          </pre>
        </div>
      </div>
    </div>
  );
}