'use client';

import React, { useState } from 'react';
import DependencyGraph from '@/components/DependencyGraph';
import { UploadDropzone } from '@/components/UploadDropzone';
import ArchitectureChatDrawer from '@/components/ArchitectureChatDrawer';
import { AnalysisResult } from '@/lib/api';
import RefactorModal from '@/components/RefactorModal';
import { applyRefactoringPatch } from '@/lib/api';
import { downloadAnalysisReport } from '@/lib/export';

export default function Home() {
  const [activeTab, setActiveTab] = useState<
    'topology' | 'uploader' | 'refactor'
  >('topology');

  const [analysisResult, setAnalysisResult] =
    useState<AnalysisResult | null>(null);

  const [isRefactoring, setIsRefactoring] = useState(false);
  const [refactorLog, setRefactorLog] = useState<string | null>(null);

  // =========================================================
  // REFACTOR MODAL & SOURCE CODE STATE
  // =========================================================
  const [isRefactorModalOpen, setIsRefactorModalOpen] = useState(false);
  const [sourceCode, setSourceCode] = useState<string>(
    '// Select or analyze a file to view source code content'
  );
  const [selectedFilePath, setSelectedFilePath] = useState<string | null>(null);
  const [refactoredCode, setRefactoredCode] = useState<string>('');
  const [isApplyingRefactor, setIsApplyingRefactor] = useState<boolean>(false);

  // =========================================================
  // CALL GRAPH STATE
  // =========================================================

  const [viewMode, setViewMode] = useState<
    'dependencies' | 'calls'
  >('dependencies');

  const [callGraphData, setCallGraphData] = useState<any[]>([]);
  const [callGraphNodes, setCallGraphNodes] = useState<any[]>([]);
  const [callGraphEdges, setCallGraphEdges] = useState<any[]>([]);
  const [isLoadingCallGraph, setIsLoadingCallGraph] = useState(false);

  // =========================================================
  // ANALYSIS COMPLETE
  // =========================================================

  const handleAnalysisComplete = (result: AnalysisResult) => {
    setAnalysisResult(result);
    setActiveTab('topology');
    setViewMode('dependencies');
    setCallGraphData([]);
    setCallGraphNodes([]);
    setCallGraphEdges([]);
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

        const nodeMap = new Map();
        const edges: any[] = [];

        data.calls.forEach((call: any, index: number) => {
          const caller =
            call.caller || call.from || call.source || 'Unknown';
          const callee =
            call.callee || call.to || call.target || 'Unknown';

          if (!nodeMap.has(caller)) {
            nodeMap.set(caller, {
              id: caller,
              data: { label: caller },
              position: { x: (index * 60) % 500, y: (index * 40) % 400 },
            });
          }
          if (!nodeMap.has(callee)) {
            nodeMap.set(callee, {
              id: callee,
              data: { label: callee },
              position: {
                x: ((index + 1) * 60) % 500,
                y: ((index + 1) * 40) % 400,
              },
            });
          }

          edges.push({
            id: `edge-${caller}-${callee}-${index}`,
            source: caller,
            target: callee,
            animated: true,
          });
        });

        setCallGraphNodes(Array.from(nodeMap.values()));
        setCallGraphEdges(edges);
      } else if (data.nodes && data.edges) {
        setCallGraphNodes(data.nodes);
        setCallGraphEdges(data.edges);
      } else {
        setCallGraphData([]);
        setCallGraphNodes([]);
        setCallGraphEdges([]);
      }
    } catch (error) {
      console.error('Call graph error:', error);
      setCallGraphData([]);
      setCallGraphNodes([]);
      setCallGraphEdges([]);
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

            <div className="flex gap-2 flex-wrap items-center">

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

              {/* Export Report */}
              {analysisResult && (
                <button
                  onClick={() => downloadAnalysisReport(analysisResult, selectedFilePath || 'source.ts')}
                  className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-200 text-xs font-medium rounded-xl border border-gray-700 transition-all flex items-center gap-2 shadow-sm"
                >
                  📥 Export Report (.md)
                </button>
              )}

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
                className="bg-purple-600 hover:bg-purple-500 text-white px-3 py-2 rounded-lg text-xs font-semibold transition flex items-center gap-1"
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
                initialNodes={(analysisResult?.graph?.nodes || []) as any}
                initialEdges={(analysisResult?.graph?.edges || []) as any}
              />
            )}

            {/* =====================================================
                CALL GRAPH
            ===================================================== */}

            {viewMode === 'calls' && (
              <div className="space-y-3">
                {isLoadingCallGraph ? (
                  <div className="bg-gray-900 border border-gray-800 p-8 rounded-xl text-center text-gray-400">
                    Analyzing call hierarchy...
                  </div>
                ) : (
                  <DependencyGraph
                    initialNodes={callGraphNodes || []}
                    initialEdges={callGraphEdges || []}
                  />
                )}
              </div>
            )}

          </div>
        )}

        {/* =========================================================
            REFACTOR TAB - ARCHITECTURAL ISSUES & AST REFACTORING
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

            {/* Refactoring Plan Banner (if available) */}
            {analysisResult?.refactoring_plan && (
              <div className="flex items-center justify-between bg-gray-950 border border-gray-800 p-4 rounded-xl">
                <div>
                  <h4 className="text-sm font-semibold text-white">Refactoring Plan Available</h4>
                  <p className="text-xs text-gray-400 mt-0.5">
                    {analysisResult.refactoring_plan.refactoring_steps?.length || 0} recommended fixes found.
                  </p>
                </div>
                <button
                  onClick={() => setIsRefactorModalOpen(true)}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium rounded-lg transition-all shadow-lg shadow-blue-600/25"
                >
                  Review Refactor Plan ✨
                </button>
              </div>
            )}

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
            ARCHITECTURE AI CHAT DRAWER
        ========================================================= */}

        <ArchitectureChatDrawer
          analysisResult={analysisResult}
        />

        {/* =========================================================
            REFACTOR MODAL COMPONENT
        ========================================================= */}
        <RefactorModal
          isOpen={isRefactorModalOpen}
          onClose={() => setIsRefactorModalOpen(false)}
          filePath={analysisResult?.refactoring_plan?.file_path || 'file.ts'}
          originalCode={sourceCode}
          refactoredCode={refactoredCode || sourceCode}
          steps={analysisResult?.refactoring_plan?.refactoring_steps || []}
          onApply={async () => {
            try {
              setIsApplyingRefactor(true);
              const res = await applyRefactoringPatch({
                file_path: analysisResult?.refactoring_plan?.file_path || 'file.ts',
                source_code: sourceCode,
                steps: analysisResult?.refactoring_plan?.refactoring_steps || [],
              });
              setRefactoredCode(res.refactored_code);
              console.log('Refactoring patch compiled successfully!');
            } catch (err) {
              console.error('Failed to apply refactoring patch:', err);
            } finally {
              setIsApplyingRefactor(false);
            }
          }}
        />

      </div>
    </main>
  );
}