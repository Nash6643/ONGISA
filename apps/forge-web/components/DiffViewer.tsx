'use client';

import React from 'react';
import ReactDiffViewer, { DiffMethod } from 'react-diff-viewer-continued';

interface DiffViewerProps {
  oldCode: string;
  newCode: string;
  filename: string;
}

export default function DiffViewer({ oldCode, newCode, filename }: DiffViewerProps) {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden p-4">
      <div className="flex justify-between items-center mb-3">
        <span className="font-mono text-xs text-cyan-400 font-bold">{filename}</span>
        <span className="text-xs text-gray-500 uppercase">AST Refactoring Diff</span>
      </div>
      <div className="rounded-lg overflow-hidden text-xs">
        <ReactDiffViewer
          oldValue={oldCode}
          newValue={newCode}
          splitView={true}
          compareMethod={DiffMethod.WORDS}
          useDarkTheme={true}
          styles={{
            variables: {
              dark: {
                diffViewerBackground: '#030712',
                gutterBackground: '#0b0f19',
                addedBackground: '#064e3b',
                removedBackground: '#7f1d1d',
              },
            },
          }}
        />
      </div>
    </div>
  );
}