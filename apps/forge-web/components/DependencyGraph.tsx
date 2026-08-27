'use client';

import React, { useEffect, useState } from 'react';

interface SymbolNode {
  name: string;
  kind: string;
  line: number;
}

interface FileData {
  path: string;
  name?: string;
  symbols?: SymbolNode[];
  imports?: string[];
}

export default function DependencyGraph() {
  const [data, setData] = useState<any>(null);
  const [selectedFile, setSelectedFile] = useState<FileData | null>(null);
  const [viewMode, setViewMode] = useState<'canvas' | 'list'>('canvas');

  useEffect(() => {
    fetch('/api/graph')
      .then((res) => res.json())
      .then((resData) => {
        if (resData && !resData.error) {
          setData(resData);
        }
      })
      .catch((err) => console.error(err));
  }, []);

  if (!data) {
    return <div className="p-8 text-gray-400">Loading codebase dependency graph...</div>;
  }

  let filesList: FileData[] = [];
  if (Array.isArray(data)) {
    filesList = data;
  } else if (Array.isArray(data.files)) {
    filesList = data.files;
  } else if (typeof data === 'object') {
    filesList = Object.entries(data).map(([filePath, fileDetails]: [string, any]) => ({
      path: filePath,
      ...(typeof fileDetails === 'object' ? fileDetails : {}),
    }));
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center bg-gray-900 p-4 rounded-xl border border-gray-800">
        <h2 className="text-xl font-bold text-cyan-400">Architecture Topology</h2>
        <div className="flex gap-2">
          <button
            onClick={() => setViewMode('canvas')}
            className={`px-3 py-1 rounded text-sm font-medium transition ${
              viewMode === 'canvas' ? 'bg-cyan-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'
            }`}
          >
            Visual Canvas
          </button>
          <button
            onClick={() => setViewMode('list')}
            className={`px-3 py-1 rounded text-sm font-medium transition ${
              viewMode === 'list' ? 'bg-cyan-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'
            }`}
          >
            Module List
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="col-span-2 bg-gray-900 border border-gray-800 rounded-xl p-4 min-h-[500px] flex flex-col justify-center items-center relative overflow-hidden">
          {viewMode === 'canvas' ? (
            <svg className="w-full h-[480px] bg-gray-950 rounded-lg border border-gray-800">
              {filesList.map((file, idx) => {
                const angle = (idx / Math.max(filesList.length, 1)) * 2 * Math.PI;
                const cx = 250 + 160 * Math.cos(angle);
                const cy = 240 + 160 * Math.sin(angle);
                const isSelected = selectedFile?.path === file.path;

                return (
                  <g key={file.path} onClick={() => setSelectedFile(file)} className="cursor-pointer">
                    <circle
                      cx={cx}
                      cy={cy}
                      r={isSelected ? 18 : 12}
                      className={`${isSelected ? 'fill-cyan-400 stroke-cyan-200' : 'fill-cyan-900 stroke-cyan-600'} transition-all`}
                      strokeWidth="2"
                    />
                    <text
                      x={cx}
                      y={cy + 28}
                      textAnchor="middle"
                      className="fill-gray-300 text-[10px] font-mono select-none"
                    >
                      {file.path.split('/').pop()}
                    </text>
                  </g>
                );
              })}
            </svg>
          ) : (
            <div className="w-full space-y-2 max-h-[480px] overflow-y-auto">
              {filesList.map((file) => (
                <div
                  key={file.path}
                  onClick={() => setSelectedFile(file)}
                  className={`p-3 rounded-lg border cursor-pointer transition ${
                    selectedFile?.path === file.path ? 'border-cyan-500 bg-cyan-950/30' : 'border-gray-800 bg-gray-950'
                  }`}
                >
                  <span className="font-mono text-sm text-gray-200">{file.path}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
          <h3 className="text-lg font-semibold text-cyan-400 mb-3">Module Details</h3>
          {selectedFile ? (
            <div className="space-y-4">
              <div>
                <span className="text-xs uppercase text-gray-500 font-bold">Path</span>
                <p className="font-mono text-sm text-white break-all">{selectedFile.path}</p>
              </div>
              <div>
                <span className="text-xs uppercase text-gray-500 font-bold">Symbols ({selectedFile.symbols?.length || 0})</span>
                <ul className="mt-1 space-y-1 max-h-36 overflow-y-auto">
                  {(selectedFile.symbols || []).map((sym, i) => (
                    <li key={i} className="text-xs font-mono text-emerald-400">
                      [{sym.kind}] {sym.name} (L{sym.line})
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ) : (
            <p className="text-sm text-gray-500">Select a module node on the canvas to inspect AST metadata.</p>
          )}
        </div>
      </div>
    </div>
  );
}