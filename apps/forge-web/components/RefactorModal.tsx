'use client';

import React, { useState } from 'react';

interface RefactorModalProps {
  isOpen: boolean;
  onClose: () => void;
  fileName: string;
  initialCode: string;
}

export default function RefactorModal({
  isOpen,
  onClose,
  fileName,
  initialCode,
}: RefactorModalProps) {
  const [code, setCode] = useState(initialCode);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  if (!isOpen) return null;

  const handleRunRefactor = async () => {
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch('/api/graph/refactor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source_code: code }),
      });
      const data = await res.json();
      setResult(data);
    } catch (e: any) {
      setResult({ status: 'error', message: e.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
      <div className="w-full max-w-3xl rounded-xl bg-slate-900 border border-slate-800 p-6 shadow-2xl text-slate-100">
        <div className="flex justify-between items-center pb-4 border-b border-slate-800">
          <h2 className="text-xl font-bold text-indigo-400">
            AST Dry-Run Refactor: <span className="text-white">{fileName}</span>
          </h2>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-100 text-lg font-semibold"
          >
            ✕
          </button>
        </div>

        <div className="mt-4 space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-1">
              Source Code
            </label>
            <textarea
              className="w-full h-40 font-mono text-sm bg-slate-950 border border-slate-800 rounded-lg p-3 text-emerald-400 focus:outline-none focus:border-indigo-500"
              value={code}
              onChange={(e) => setCode(e.target.value)}
            />
          </div>

          <button
            onClick={handleRunRefactor}
            disabled={loading}
            className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-700 font-semibold rounded-lg transition-colors"
          >
            {loading ? 'Running AST Analysis...' : 'Run AST Refactor Dry-Run'}
          </button>

          {result && (
            <div className="mt-4 p-4 rounded-lg bg-slate-950 border border-slate-800 text-sm space-y-2 max-h-60 overflow-y-auto">
              <h3 className="font-semibold text-indigo-300">Analysis Results</h3>
              {result.status === 'error' ? (
                <p className="text-red-400">{result.message}</p>
              ) : (
                <>
                  <p className="text-slate-300">
                    <span className="text-indigo-400">Total Functions:</span>{' '}
                    {result.total_functions} |{' '}
                    <span className="text-indigo-400">Total Imports:</span>{' '}
                    {result.total_imports}
                  </p>
                  <div>
                    <span className="font-semibold text-slate-300">
                      Transformations / Suggestions:
                    </span>
                    <ul className="list-disc list-inside text-slate-400 mt-1 space-y-1">
                      {result.transformations?.map((t: string, idx: number) => (
                        <li key={idx}>{t}</li>
                      ))}
                    </ul>
                  </div>
                  {result.refactored_code_preview && (
                    <div className="mt-2">
                      <span className="font-semibold text-slate-300">
                        Refactored Preview:
                      </span>
                      <pre className="mt-1 p-2 bg-slate-900 border border-slate-800 rounded font-mono text-xs text-emerald-300 overflow-x-auto">
                        {result.refactored_code_preview}
                      </pre>
                    </div>
                  )}
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}