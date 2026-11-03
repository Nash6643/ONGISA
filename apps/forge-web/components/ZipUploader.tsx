"use client";

import React, { useState } from "react";

interface Issue {
  severity: string;
  issue_type: string;
  target: string;
  description: string;
}

interface AnalysisResult {
  status: string;
  filename: string;
  total_files: number;
  issues: Issue[];
}

export default function ZipUploader() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/analyze/zip", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Server returned error status: ${res.status}`);
      }

      const data: AnalysisResult = await res.json();
      setResult(data);
    } catch (err) {
      console.error("Failed to analyze zip archive:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl max-w-xl mx-auto text-white">
      <h3 className="text-xl font-bold mb-4">Analyze Repository Zip Archive</h3>
      
      <input
        type="file"
        accept=".zip"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="block w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-cyan-600 file:text-white hover:file:bg-cyan-500 cursor-pointer mb-4"
      />

      <button
        onClick={handleUpload}
        disabled={!file || loading}
        className="w-full py-2 rounded-lg bg-cyan-500 hover:bg-cyan-400 font-semibold disabled:opacity-50 transition"
      >
        {loading ? "Analyzing Codebase..." : "Upload & Analyze .zip"}
      </button>

      {result && (
        <div className="mt-6 p-4 bg-slate-950 rounded-lg border border-slate-800 text-sm">
          <p className="text-emerald-400 font-bold">Analysis Complete!</p>
          <p className="mt-1">Uploaded: {result.filename}</p>
          <p className="mt-1">Files Scanned: {result.total_files}</p>
          <p className="mt-1">Architectural Issues: {result.issues.length}</p>

          {result.issues.length > 0 && (
            <div className="mt-4 space-y-2">
              <p className="font-semibold text-slate-300">Detected Issues:</p>
              {result.issues.map((issue, idx) => (
                <div key={idx} className="p-2 rounded bg-slate-900 border border-slate-800">
                  <span className="text-red-400 font-bold">[{issue.severity}]</span>{" "}
                  <span className="text-yellow-400">{issue.issue_type}</span> on{" "}
                  <span className="text-cyan-300">{issue.target}</span>: {issue.description}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}