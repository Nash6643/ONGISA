'use client';

import React, { useState } from 'react';
import DependencyGraph from '@/components/DependencyGraph';
import ZipUploader from "@/components/ZipUploader";

export default function Home() {
  const [activeTab, setActiveTab] = useState<'topology' | 'uploader' | 'refactor'>('topology');
  const [isRefactoring, setIsRefactoring] = useState(false);
  const [refactorLog, setRefactorLog] = useState<string | null>(null);

  const runRefactorDryRun = async () => {
    setIsRefactoring(true);
    setRefactorLog(null);
    try {
      const res = await fetch('/api/refactor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ targetFile: '.', rule: 'all' }),
      });
      const data = await res.json();
      setRefactorLog(data.output || data.error || 'Refactor completed.');
    } catch (err) {
      setRefactorLog('Error executing refactoring engine.');
    } finally {
      setIsRefactoring(false);
    }
  };

  return (
    <main className="min-h-screen p-8 bg-gray-950 text-gray-100">
      <div className="max-w-7xl mx-auto space-y-6">
        <header className="border-b border-gray-800 pb-4 flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white">
              ONGISA Architecture Dashboard
            </h1>
            <p className="text-sm text-gray-400 mt-1">
              Omar Nashiru-deen GitHub Statistical Analyzer — Static analysis & symbol tree mapping.
            </p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setActiveTab('topology')}
              className={`px-4 py-2 rounded-lg font-medium text-sm transition ${
                activeTab === 'topology'
                  ? 'bg-cyan-600 text-white'
                  : 'bg-gray-900 text-gray-400 border border-gray-800 hover:text-white'
              }`}
            >
              Topology Graph
            </button>
            <button
              onClick={() => setActiveTab('uploader')}
              className={`px-4 py-2 rounded-lg font-medium text-sm transition ${
                activeTab === 'uploader'
                  ? 'bg-cyan-600 text-white'
                  : 'bg-gray-900 text-gray-400 border border-gray-800 hover:text-white'
              }`}
            >
              Zip Analyzer
            </button>
            <button
              onClick={() => setActiveTab('refactor')}
              className={`px-4 py-2 rounded-lg font-medium text-sm transition ${
                activeTab === 'refactor'
                  ? 'bg-cyan-600 text-white'
                  : 'bg-gray-900 text-gray-400 border border-gray-800 hover:text-white'
              }`}
            >
              Code Smells & Refactoring
            </button>
          </div>
        </header>

        {activeTab === 'topology' && <DependencyGraph />}

        {activeTab === 'uploader' && (
          <div className="py-4">
            <ZipUploader />
          </div>
        )}

        {activeTab === 'refactor' && (
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 space-y-4">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-xl font-bold text-cyan-400">AST Automated Refactoring</h2>
                <p className="text-sm text-gray-400">
                  Run static analyzer transformations across your C++ / Python / Rust dependencies.
                </p>
              </div>
              <button
                onClick={runRefactorDryRun}
                disabled={isRefactoring}
                className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-semibold transition disabled:opacity-50"
              >
                {isRefactoring ? 'Analyzing Codebase...' : 'Run Dry-Run Refactor'}
              </button>
            </div>

            <div className="bg-gray-950 border border-gray-800 rounded-lg p-4 font-mono text-xs max-h-96 overflow-y-auto">
              {refactorLog ? (
                <pre className="text-emerald-400 whitespace-pre-wrap">{refactorLog}</pre>
              ) : (
                <p className="text-gray-600">Click "Run Dry-Run Refactor" to preview code smell updates...</p>
              )}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}