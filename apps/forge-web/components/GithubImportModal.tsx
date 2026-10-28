'use client';

import React, { useState } from 'react';
import { analyzeGitHubRepository } from '@/lib/github_api';

interface GitHubImportModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: (result: any) => void; // Add this line
}

export default function GitHubImportModal({ isOpen, onClose }: GitHubImportModalProps) {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [resultMessage, setResultMessage] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await analyzeGitHubRepository(url);
      setResultMessage(`Success! Cloned ${res.repo} from ${res.owner}.`);
    } catch (err: any) {
      setResultMessage(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 border border-gray-800 rounded-2xl max-w-md w-full p-6 shadow-2xl">
        <h3 className="text-white font-mono text-lg font-bold mb-2">🐙 Import GitHub Repository</h3>
        <p className="text-gray-400 text-xs mb-4">Paste a public GitHub repository URL to analyze its architecture and smells instantly.</p>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            placeholder="[https://github.com/owner/repo](https://github.com/owner/repo)"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-2.5 text-sm text-gray-200 font-mono focus:outline-none focus:border-blue-600"
          />
          <div className="flex justify-end space-x-3">
            <button type="button" onClick={onClose} className="px-4 py-2 text-xs font-mono text-gray-400 hover:text-white">Cancel</button>
            <button type="submit" disabled={loading} className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-mono rounded-xl font-bold">
              {loading ? 'Cloning...' : 'Analyze Repo'}
            </button>
          </div>
        </form>
        {resultMessage && <p className="mt-4 text-xs font-mono text-emerald-400">{resultMessage}</p>}
      </div>
    </div>
  );
}