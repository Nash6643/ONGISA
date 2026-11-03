'use client';

import React from 'react';
import { RefactoringStep } from '../lib/api';
import DiffViewer from './DiffViewer';

interface RefactorModalProps {
  isOpen: boolean;
  onClose: () => void;
  filePath: string;
  originalCode: string;
  refactoredCode?: string;
  steps: RefactoringStep[];
  onApply: () => void;
}

export default function RefactorModal({
  isOpen,
  onClose,
  filePath,
  originalCode,
  refactoredCode = originalCode,
  steps,
  onApply,
}: RefactorModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
      <div className="bg-gray-900 border border-gray-800 rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-gray-800 flex items-center justify-between bg-gray-950">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              ✨ AI Refactoring Plan
            </h2>
            <p className="text-xs text-gray-400 font-mono mt-0.5">{filePath}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors p-1 rounded-lg hover:bg-gray-800"
          >
            ✕
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1">
          {/* Refactoring Steps breakdown */}
          <div>
            <h3 className="text-sm font-semibold text-gray-300 mb-3">Recommended Actions ({steps.length})</h3>
            <div className="space-y-3">
              {steps.map((step, idx) => (
                <div key={idx} className="bg-gray-950 border border-gray-800 p-4 rounded-xl space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono px-2 py-0.5 bg-blue-950 text-blue-400 border border-blue-900 rounded">
                      Line {step.target_line}: {step.action}
                    </span>
                  </div>
                  <p className="text-sm text-gray-200">{step.description}</p>
                  <div className="text-xs font-mono text-emerald-400 bg-emerald-950/30 p-2 rounded border border-emerald-900/30">
                    💡 Suggestion: {step.suggestion}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Diff Preview */}
          <div>
            <h3 className="text-sm font-semibold text-gray-300 mb-3">Code Diff Preview</h3>
            <DiffViewer originalCode={originalCode} refactoredCode={refactoredCode} filePath={filePath} />
          </div>
        </div>

        {/* Modal Footer */}
        <div className="px-6 py-4 border-t border-gray-800 bg-gray-950 flex items-center justify-end space-x-3">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm text-gray-400 hover:text-white transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={() => {
              onApply();
              onClose();
            }}
            className="px-5 py-2 text-sm font-medium bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl transition-all shadow-lg shadow-emerald-600/20"
          >
            Apply Refactoring Patch
          </button>
        </div>

      </div>
    </div>
  );
}