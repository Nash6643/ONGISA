"use client";

import React, { useState } from "react";
import { uploadZipForAnalysis, AnalysisResult } from "@/lib/api";

interface UploadDropzoneProps {
  onAnalysisComplete?: (result: AnalysisResult) => void;
}

export const UploadDropzone: React.FC<UploadDropzoneProps> = ({ onAnalysisComplete }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      const result = await uploadZipForAnalysis(file);
      if (onAnalysisComplete) {
        onAnalysisComplete(result);
      }
    } catch (err: any) {
      setError(err.message || "An error occurred during upload.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="border-2 border-dashed border-gray-700 rounded-xl p-8 text-center bg-gray-900/50">
      <input
        type="file"
        accept=".zip"
        onChange={handleFileChange}
        className="hidden"
        id="zip-upload-input"
        disabled={loading}
      />
      <label htmlFor="zip-upload-input" className="cursor-pointer block">
        {loading ? (
          <p className="text-blue-400 font-medium animate-pulse">Analyzing repository dependency graph...</p>
        ) : (
          <div>
            <p className="text-gray-200 font-medium">Click or drag a .zip repository archive here</p>
            <p className="text-sm text-gray-500 mt-1">Supports Python, TypeScript, JavaScript, and Rust</p>
          </div>
        )}
      </label>
      {error && <p className="text-red-400 mt-4 text-sm">{error}</p>}
    </div>
  );
};