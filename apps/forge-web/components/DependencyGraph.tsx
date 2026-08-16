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
  extension?: string;
  size_bytes?: number;
  symbols?: SymbolNode[];
  imports?: string[];
}

export default function DependencyGraph() {
  const [data, setData] = useState<any>(null);
  const [selectedFile, setSelectedFile] = useState<FileData | null>(null);

  useEffect(() => {
    fetch('/api/graph')
      .then((res) => res.json())
      .then((resData) => {
        if (resData && !resData.error) {
          setData(resData);
        } else {
          console.error('Graph API Error:', resData?.error);
        }
      })
      .catch((err) => console.error(err));
  }, []);

  if (!data) {
    return <div className="p-8 text-gray-400">Loading codebase dependency graph...</div>;
  }

  // Parse files list dynamically based on json schema
  let filesList: FileData[] = [];
  if (Array.isArray(data)) {
    filesList = data;
  } else if (Array.isArray(data.files)) {
    filesList = data.files;
  } else if (typeof data === 'object') {
    // Handle dictionary structure where keys are file paths
    filesList = Object.entries(data).map(([filePath, fileDetails]: [string, any]) => ({
      path: filePath,
      ...(typeof fileDetails === 'object' ? fileDetails : {}),
    }));
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 p-6">
      <div className="col-span-2 bg-gray-900 border border-gray-800 rounded-xl p-4">
        <h2 className="text-xl font-semibold mb-4 text-cyan-400">
          Project Modules ({filesList.length})
        </h2>
        
        {filesList.length === 0 ? (
          <p className="text-sm text-gray-500">No file data found in graph.json. Run CLI analysis first.</p>
        ) : (
          <div className="space-y-2 max-h-[600px] overflow-y-auto">
            {filesList.map((file) => (
              <div
                key={file.path}
                onClick={() => setSelectedFile(file)}
                className={`p-3 rounded-lg border cursor-pointer transition ${
                  selectedFile?.path === file.path
                    ? 'border-cyan-500 bg-cyan-950/30'
                    : 'border-gray-800 bg-gray-950 hover:border-gray-700'
                }`}
              >
                <div className="flex justify-between items-center">
                  <span className="font-mono text-sm text-gray-200">{file.path}</span>
                  {file.size_bytes !== undefined && (
                    <span className="text-xs text-gray-500">
                      {(file.size_bytes / 1024).toFixed(1)} KB
                    </span>
                  )}
                </div>
                <div className="flex gap-2 mt-2">
                  <span className="text-xs bg-gray-800 px-2 py-0.5 rounded text-gray-400">
                    {(file.symbols || []).length} symbols
                  </span>
                  <span className="text-xs bg-gray-800 px-2 py-0.5 rounded text-gray-400">
                    {(file.imports || []).length} imports
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
        <h2 className="text-xl font-semibold mb-4 text-cyan-400">Module Details</h2>
        {selectedFile ? (
          <div>
            <h3 className="font-mono text-sm font-bold text-white mb-2">{selectedFile.path}</h3>
            <div className="mb-4">
              <h4 className="text-xs uppercase text-gray-500 font-semibold mb-1">Exported Symbols</h4>
              <ul className="space-y-1 max-h-40 overflow-y-auto">
                {(selectedFile.symbols || []).length > 0 ? (
                  selectedFile.symbols?.map((sym, i) => (
                    <li key={i} className="text-xs font-mono text-emerald-400">
                      [{sym.kind}] {sym.name} (L{sym.line})
                    </li>
                  ))
                ) : (
                  <li className="text-xs text-gray-500">No symbols detected</li>
                )}
              </ul>
            </div>
            <div>
              <h4 className="text-xs uppercase text-gray-500 font-semibold mb-1">Imports</h4>
              <ul className="space-y-1 max-h-40 overflow-y-auto">
                {(selectedFile.imports || []).length > 0 ? (
                  selectedFile.imports?.map((imp, i) => (
                    <li key={i} className="text-xs font-mono text-gray-400">
                      ➔ {imp}
                    </li>
                  ))
                ) : (
                  <li className="text-xs text-gray-500">No imports detected</li>
                )}
              </ul>
            </div>
          </div>
        ) : (
          <p className="text-sm text-gray-500">Select a file from the list to view AST symbols and dependencies.</p>
        )}
      </div>
    </div>
  );
}