'use client';

import React, { useState } from 'react';
import DependencyGraph from '@/components/DependencyGraph';
import { UploadDropzone } from '@/components/UploadDropzone';
import ArchitectureChatDrawer from '@/components/ArchitectureChatDrawer';
import { AnalysisResult } from '@/lib/api';

export default function Home() {
  const [activeTab, setActiveTab] = useState<
    'topology' | 'uploader' | 'refactor'
  >('topology');

  const [analysisResult, setAnalysisResult] =
    useState<AnalysisResult | null>(null);

  const [isRefactoring, setIsRefactoring] = useState(false);
  const [refactorLog, setRefactorLog] = useState<string | null>(null);

  const handleAnalysisComplete = (result: AnalysisResult) => {
    setAnalysisResult(result);
    setActiveTab('topology');
  };

  const runRefactorDryRun = async () => {
    setIsRefactoring(true);
    setRefactorLog(null);

    try {
      const res = await fetch('/api/refactor', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          targetFile: '.',
          rule: 'all',
        }),
      });

      const data = await res.json();

      setRefactorLog(
        data.output || data.error || 'Refactor completed.'
      );
    } catch {
      setRefactorLog('Error executing refactoring engine.');
    } finally {
      setIsRefactoring(false);
    }
  };

  return (
    <main className="min-h-screen p-8 bg-gray-950 text-gray-100">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <header className="border-b border-gray-800 pb-4 flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white">
              ONGISA Architecture Dashboard
            </h1>

            <p className="text-sm text-gray-400 mt-1">
              Omar Nashiru-deen GitHub Statistical Analyzer — Static analysis
              & symbol tree mapping.
            </p>
          </div>

          <div className="flex gap-2">

            {/* Topology */}
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

            {/* Uploader */}
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

            {/* Refactor */}
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

        {/* =========================================================
            TOPOLOGY TAB
        ========================================================= */}

        {activeTab === 'topology' && (
          <DependencyGraph
            initialNodes={analysisResult?.graph.nodes}
            initialEdges={analysisResult?.graph.edges}
          />
        )}

        {/* =========================================================
            REFACTOR TAB - ARCHITECTURAL ISSUES
        ========================================================= */}

        {activeTab === 'refactor' && (
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 space-y-6">

            <div className="flex justify-between items-center border-b border-gray-800 pb-4">
              <div>
                <h2 className="text-xl font-bold text-cyan-400">
                  Architectural Issues & AST Refactoring
                </h2>

                <p className="text-sm text-gray-400">
                  Detected circular imports, high coupling, and god modules
                  across scanned codebases.
                </p>
              </div>

              <button
                onClick={runRefactorDryRun}
                disabled={isRefactoring}
                className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-semibold transition disabled:opacity-50"
              >
                {isRefactoring
                  ? 'Analyzing Codebase...'
                  : 'Run Dry-Run Refactor'}
              </button>
            </div>

            {/* Detected Code Smells List */}
            <div className="space-y-3">

              <h3 className="text-xs font-semibold uppercase text-gray-400 tracking-wider">
                Detected Code Smells
              </h3>

              {analysisResult?.issues &&
              analysisResult.issues.length > 0 ? (
                <div className="grid gap-3">

                  {analysisResult.issues.map((issue, idx) => (
                    <div
                      key={idx}
                      className={`p-4 rounded-lg border ${
                        issue.severity === 'high'
                          ? 'bg-red-950/30 border-red-800 text-red-200'
                          : 'bg-amber-950/30 border-amber-800 text-amber-200'
                      }`}
                    >

                      <div className="flex items-center justify-between">

                        <span className="font-mono text-xs uppercase px-2 py-0.5 rounded bg-black/40">
                          {issue.type}
                        </span>

                        <span className="text-xs font-semibold capitalize">
                          {issue.severity} severity
                        </span>

                      </div>

                      <p className="text-sm mt-2 font-mono">
                        {issue.description}
                      </p>

                    </div>
                  ))}

                </div>
              ) : (
                <p className="text-xs text-gray-500 italic">
                  No architectural code smells detected yet. Upload a
                  repository .zip file in the Zip Analyzer tab to run
                  detection.
                </p>
              )}

            </div>

            {/* Dry Run Output Console */}
            <div className="bg-gray-950 border border-gray-800 rounded-lg p-4 font-mono text-xs max-h-96 overflow-y-auto">

              {refactorLog ? (
                <pre className="text-emerald-400 whitespace-pre-wrap">
                  {refactorLog}
                </pre>
              ) : (
                <p className="text-gray-600">
                  Click "Run Dry-Run Refactor" to preview AST code
                  transformations...
                </p>
              )}

            </div>

          </div>
        )}

        {/* =========================================================
            UPLOADER TAB
        ========================================================= */}
{activeTab === 'uploader' && (
  <div className="py-4 space-y-6">

    {/* Git Repository Analyzer */}
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">

      <h2 className="text-xl font-bold text-cyan-400 mb-2">
        Analyze Git Repository
      </h2>

      <p className="text-sm text-gray-400 mb-4">
        Enter a public GitHub repository URL to clone and analyze its architecture.
      </p>

      <div className="flex gap-2 items-center mb-4">
        <input
          type="text"
          placeholder="https://github.com/username/repository"
          className="bg-gray-900 border border-gray-800 rounded-lg px-3 py-2 text-xs text-white font-mono flex-1"
          id="repoUrlInput"
        />

        <button
          onClick={async () => {
            const inputEl = document.getElementById(
              'repoUrlInput'
            ) as HTMLInputElement;

            if (!inputEl?.value) return;

            // Trigger API call to /api/analyze/git
          }}
          className="bg-cyan-600 hover:bg-cyan-500 text-white px-4 py-2 rounded-lg text-xs font-semibold transition"
        >
          Clone & Analyze Repo
        </button>
      </div>

    </div>

    {/* ZIP Analyzer */}
    <UploadDropzone
      onAnalysisComplete={handleAnalysisComplete}
    />

  </div>
)}

        {/* =========================================================
            REFACTOR TAB - AST AUTOMATED REFACTORING
        ========================================================= */}

        {activeTab === 'refactor' && (
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 space-y-4">

            <div className="flex justify-between items-center">

              <div>
                <h2 className="text-xl font-bold text-cyan-400">
                  AST Automated Refactoring
                </h2>

                <p className="text-sm text-gray-400">
                  Run static analyzer transformations across your C++ /
                  Python / Rust dependencies.
                </p>
              </div>

              <button
                onClick={runRefactorDryRun}
                disabled={isRefactoring}
                className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-semibold transition disabled:opacity-50"
              >
                {isRefactoring
                  ? 'Analyzing Codebase...'
                  : 'Run Dry-Run Refactor'}
              </button>

            </div>

            <div className="bg-gray-950 border border-gray-800 rounded-lg p-4 font-mono text-xs max-h-96 overflow-y-auto">

              {refactorLog ? (
                <pre className="text-emerald-400 whitespace-pre-wrap">
                  {refactorLog}
                </pre>
              ) : (
                <p className="text-gray-600">
                  Click "Run Dry-Run Refactor" to preview code smell
                  updates...
                </p>
              )}

            </div>

          </div>
        )}

        {/* =========================================================
            ARCHITECTURE AI CHAT DRAWER
        ========================================================= */}

        <ArchitectureChatDrawer
          analysisResult={analysisResult}
        />

      </div>
    </main>
  );
}
