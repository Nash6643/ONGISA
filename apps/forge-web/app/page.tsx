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

  // =========================================================
  // CALL GRAPH STATE
  // =========================================================

  const [viewMode, setViewMode] = useState<
    'dependencies' | 'calls'
  >('dependencies');

  const [callGraphData, setCallGraphData] = useState<any[]>([]);
  const [isLoadingCallGraph, setIsLoadingCallGraph] = useState(false);

  // =========================================================
  // ANALYSIS COMPLETE
  // =========================================================

  const handleAnalysisComplete = (result: AnalysisResult) => {
    setAnalysisResult(result);
    setActiveTab('topology');
    setViewMode('dependencies');
    setCallGraphData([]);
  };

  // =========================================================
  // FETCH CALL GRAPH
  // =========================================================

  const fetchCallGraph = async () => {
    if (!analysisResult) {
      return;
    }

    setIsLoadingCallGraph(true);

    try {
      const res = await fetch('/api/callgraph', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          codebase_context: analysisResult,
        }),
      });

      if (!res.ok) {
        throw new Error('Failed to fetch call graph.');
      }

      const data = await res.json();

      if (data.calls) {
        setCallGraphData(data.calls);
      } else {
        setCallGraphData([]);
      }
    } catch (error) {
      console.error('Call graph error:', error);
      setCallGraphData([]);
    } finally {
      setIsLoadingCallGraph(false);
    }
  };

  // =========================================================
  // REFACTOR
  // =========================================================

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

  // =========================================================
  // GITHUB REPOSITORY ANALYSIS
  // =========================================================

  const analyzeGitRepository = async () => {
    const inputEl = document.getElementById(
      'githubRepoInput'
    ) as HTMLInputElement;

    if (!inputEl?.value.trim()) {
      alert('Please enter a GitHub repository URL.');
      return;
    }

    try {
      const res = await fetch('/api/analyze/git', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          repo_url: inputEl.value.trim(),
        }),
      });

      const data = await res.json();

      console.log('Git Analysis Result:', data);

      if (!res.ok) {
        alert(data.message || data.error || 'Repository analysis failed.');
        return;
      }

      alert(
        data.message || 'Repository analyzed successfully!'
      );
    } catch (error) {
      console.error('Git analysis error:', error);
      alert('Failed to connect to the Git analysis API.');
    }
  };

  return (
    <main className="min-h-screen p-8 bg-gray-950 text-gray-100">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* =========================================================
            HEADER
        ========================================================= */}

        <header className="border-b border-gray-800 pb-6">

          <div className="flex justify-between items-end gap-6">

            <div>
              <h1 className="text-3xl font-bold tracking-tight text-white">
                ONGISA Architecture Dashboard
              </h1>

              <p className="text-sm text-gray-400 mt-1">
                ONGISA — Static analysis
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

              {/* Export */}
              <button
                onClick={async () => {
                  const res = await fetch('/api/export', {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                      codebase_context: analysisResult,
                    }),
                  });

                  const blob = await res.blob();
                  const url = window.URL.createObjectURL(blob);

                  const a = document.createElement('a');
                  a.href = url;
                  a.download = 'ongisa-architecture-report.md';
                  a.click();

                  window.URL.revokeObjectURL(url);
                }}
                className="bg-cyan-600 hover:bg-cyan-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5"
              >
                <span>📥</span>
                Export Audit Report
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

              <button
  onClick={async () => {
    const res = await fetch('/api/refactor', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        file_path: 'src/services/UserManager.ts',
        code_content: '// sample content or active file content',
        issue_description: 'God Module detected: high function count and tight coupling.',
      }),
    });
    const data = await res.json();
    alert(data.refactoring_plan || 'Refactoring plan generated successfully!');
  }}
  className="bg-purple-600 hover:bg-purple-500 text-white px-3 py-1 rounded text-xs font-semibold transition flex items-center gap-1"
>
  <span>🛠️</span> AI Refactor Plan
</button>

            </div>
          </div>

          {/* =========================================================
              GITHUB REPOSITORY INPUT
          ========================================================= */}

          <div className="flex gap-2 items-center bg-gray-900 p-2 rounded-xl border border-gray-800 mt-6">

            <input
              type="text"
              id="githubRepoInput"
              placeholder="https://github.com/owner/repository"
              className="bg-gray-950 border border-gray-800 rounded-lg px-3 py-2 text-xs text-white font-mono flex-1 focus:outline-none focus:border-cyan-500"
              onKeyDown={(event) => {
                if (event.key === 'Enter') {
                  analyzeGitRepository();
                }
              }}
            />

            <button
              onClick={analyzeGitRepository}
              className="bg-cyan-600 hover:bg-cyan-500 text-white px-4 py-2 rounded-lg text-xs font-semibold transition flex items-center gap-1.5"
            >
              <span>🚀</span>
              Clone & Analyze
            </button>

          </div>

        </header>

        {/* =========================================================
            TOPOLOGY TAB
        ========================================================= */}

        {activeTab === 'topology' && (
          <div className="space-y-4">

            {/* =====================================================
                GRAPH VIEW TOGGLE
            ===================================================== */}

            <div className="flex items-center justify-between">

              <div>
                <h2 className="text-lg font-semibold text-white">
                  {viewMode === 'dependencies'
                    ? 'File Dependency Graph'
                    : 'Function Call Graph'}
                </h2>

                <p className="text-xs text-gray-500 mt-1">
                  {viewMode === 'dependencies'
                    ? 'Visualize how files and modules depend on each other.'
                    : 'Visualize function-to-function call relationships.'}
                </p>
              </div>

              <div className="flex gap-2 bg-gray-950 p-1 rounded-lg border border-gray-800">

                {/* File Dependencies */}
                <button
                  onClick={() => setViewMode('dependencies')}
                  className={`px-3 py-1 rounded text-xs font-medium transition ${
                    viewMode === 'dependencies'
                      ? 'bg-cyan-600 text-white'
                      : 'text-gray-400 hover:text-white'
                  }`}
                >
                  📁 File Dependencies
                </button>

                {/* Function Call Graph */}
                <button
                  onClick={() => {
                    setViewMode('calls');
                    fetchCallGraph();
                  }}
                  disabled={!analysisResult || isLoadingCallGraph}
                  className={`px-3 py-1 rounded text-xs font-medium transition ${
                    viewMode === 'calls'
                      ? 'bg-cyan-600 text-white'
                      : 'text-gray-400 hover:text-white'
                  } ${
                    !analysisResult || isLoadingCallGraph
                      ? 'opacity-50 cursor-not-allowed'
                      : ''
                  }`}
                >
                  ⚡{' '}
                  {isLoadingCallGraph
                    ? 'Loading...'
                    : 'Function Call-Graph'}
                </button>

              </div>
            </div>

            {/* =====================================================
                DEPENDENCY GRAPH
            ===================================================== */}

            {viewMode === 'dependencies' && (
              <DependencyGraph
                initialNodes={analysisResult?.graph.nodes}
                initialEdges={analysisResult?.graph.edges}
              />
            )}

            {/* =====================================================
                CALL GRAPH
            ===================================================== */}

            {viewMode === 'calls' && (
              <div className="space-y-3">

                {!analysisResult && (
                  <div className="bg-gray-900 border border-gray-800 rounded-xl p-8 text-center">
                    <p className="text-gray-400 text-sm">
                      Upload and analyze a repository first to generate
                      the function call graph.
                    </p>
                  </div>
                )}

                {isLoadingCallGraph && (
                  <div className="bg-gray-900 border border-gray-800 rounded-xl p-8 text-center">
                    <div className="text-cyan-400 text-sm font-medium">
                      ⚡ Analyzing function call references...
                    </div>

                    <p className="text-gray-500 text-xs mt-2">
                      ONGISA is building the function-level call graph.
                    </p>
                  </div>
                )}

                {!isLoadingCallGraph &&
                  analysisResult &&
                  callGraphData.length === 0 && (
                    <div className="bg-gray-900 border border-gray-800 rounded-xl p-8 text-center">
                      <p className="text-gray-400 text-sm">
                        No function call references were returned.
                      </p>

                      <button
                        onClick={fetchCallGraph}
                        className="mt-4 px-4 py-2 bg-cyan-600 hover:bg-cyan-500 rounded-lg text-xs font-semibold transition"
                      >
                        Retry Call Graph
                      </button>
                    </div>
                  )}

                {!isLoadingCallGraph &&
                  callGraphData.length > 0 && (
                    <div className="space-y-4">

                      {/* Call Graph Summary */}
                      <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
                        <div className="flex items-center justify-between">

                          <div>
                            <h3 className="text-sm font-semibold text-cyan-400">
                              Function Call References
                            </h3>

                            <p className="text-xs text-gray-500 mt-1">
                              {callGraphData.length} call references detected.
                            </p>
                          </div>

                          <span className="text-xs font-mono bg-gray-950 border border-gray-800 px-2 py-1 rounded">
                            {callGraphData.length} calls
                          </span>

                        </div>
                      </div>

                      {/* Call Graph Data */}
                      <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
                        <div className="space-y-2">

                          {callGraphData.map((call, index) => (
                            <div
                              key={index}
                              className="bg-gray-950 border border-gray-800 rounded-lg p-3"
                            >
                              <div className="flex items-center gap-3">

                                <span className="text-cyan-400 font-mono text-xs">
                                  {call.caller ||
                                    call.from ||
                                    call.source ||
                                    'Unknown'}
                                </span>

                                <span className="text-gray-600">
                                  →
                                </span>

                                <span className="text-emerald-400 font-mono text-xs">
                                  {call.callee ||
                                    call.to ||
                                    call.target ||
                                    'Unknown'}
                                </span>

                              </div>

                              {call.file && (
                                <p className="text-[10px] text-gray-600 mt-2 font-mono">
                                  {call.file}
                                </p>
                              )}

                            </div>
                          ))}

                        </div>
                      </div>

                    </div>
                  )}

              </div>
            )}

          </div>
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

