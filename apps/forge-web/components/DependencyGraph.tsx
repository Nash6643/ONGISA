"use client";

import React, { useState, useMemo } from "react";

export interface GraphNode {
  id: string;
  name?: string;
  sizeBytes?: number;
  symbolCount?: number;
  language?: string;
  type?: string;
}

export interface GraphEdge {
  source: string;
  target: string;
  relation?: string;
}

export interface DependencyGraphProps {
  nodes?: GraphNode[];
  edges?: GraphEdge[];
  onSelectNode?: (nodeId: string) => void;
}

export const DependencyGraph: React.FC<DependencyGraphProps> = ({
  nodes = [],
  edges = [],
  onSelectNode,
}) => {
  // Filter States
  const [minFileSize, setMinFileSize] = useState<number>(0);
  const [minSymbolCount, setMinSymbolCount] = useState<number>(0);
  const [selectedLang, setSelectedLang] = useState<string>("ALL");
  const [searchQuery, setSearchQuery] = useState<string>("");

  // Calculate dynamic languages
  const availableLanguages = useMemo(() => {
    const langs = new Set<string>();
    nodes.forEach((n) => {
      if (n.language) langs.add(n.language);
    });
    return ["ALL", ...Array.from(langs)];
  }, [nodes]);

  // Max bounds for sliders
  const maxFileSize = useMemo(() => {
    return nodes.reduce((max, n) => Math.max(max, n.sizeBytes || 0), 10000);
  }, [nodes]);

  const maxSymbols = useMemo(() => {
    return nodes.reduce((max, n) => Math.max(max, n.symbolCount || 0), 20);
  }, [nodes]);

  // Compute Filtered Nodes & Edges
  const { filteredNodes, filteredEdges } = useMemo(() => {
    const activeIds = new Set<string>();

    const filteredN = nodes.filter((node) => {
      const nodeSize = node.sizeBytes || 0;
      const nodeSymbols = node.symbolCount || 0;
      const nodeLang = node.language || "Unknown";

      const matchesSize = nodeSize >= minFileSize;
      const matchesSymbols = nodeSymbols >= minSymbolCount;
      const matchesLang =
        selectedLang === "ALL" || nodeLang.toLowerCase() === selectedLang.toLowerCase();
      const matchesSearch =
        !searchQuery ||
        node.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (node.name && node.name.toLowerCase().includes(searchQuery.toLowerCase()));

      const passes = matchesSize && matchesSymbols && matchesLang && matchesSearch;
      if (passes) {
        activeIds.add(node.id);
      }
      return passes;
    });

    // Prune edges pointing to/from filtered nodes
    const filteredE = edges.filter(
      (e) => activeIds.has(e.source) && activeIds.has(e.target)
    );

    return { filteredNodes: filteredN, filteredEdges: filteredE };
  }, [nodes, edges, minFileSize, minSymbolCount, selectedLang, searchQuery]);

  return (
    <div className="flex flex-col w-full h-full bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
      {/* Control Bar Header */}
      <div className="p-4 bg-slate-800/80 backdrop-blur border-b border-slate-700/60 flex flex-col gap-3">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse" />
            Dependency Topology Controls
          </h3>
          <span className="text-xs text-slate-400 font-mono">
            Showing <strong className="text-cyan-400">{filteredNodes.length}</strong> / {nodes.length} nodes (
            <strong className="text-cyan-400">{filteredEdges.length}</strong> edges)
          </span>
        </div>

        {/* Filter Sliders and Inputs */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
          {/* File Search */}
          <div className="flex flex-col gap-1">
            <label className="text-xs font-medium text-slate-400">Search Module</label>
            <input
              type="text"
              placeholder="Filter by path..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="bg-slate-900 border border-slate-700 rounded px-2.5 py-1 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 transition-colors"
            />
          </div>

          {/* Min Size Slider */}
          <div className="flex flex-col gap-1">
            <div className="flex justify-between text-xs font-medium text-slate-400">
              <span>Min Size</span>
              <span className="text-cyan-400 font-mono">
                {(minFileSize / 1024).toFixed(1)} KB
              </span>
            </div>
            <input
              type="range"
              min={0}
              max={maxFileSize}
              step={100}
              value={minFileSize}
              onChange={(e) => setMinFileSize(Number(e.target.value))}
              className="accent-cyan-500 cursor-pointer h-1.5 bg-slate-700 rounded-lg appearance-none mt-1"
            />
          </div>

          {/* Min Symbols Slider */}
          <div className="flex flex-col gap-1">
            <div className="flex justify-between text-xs font-medium text-slate-400">
              <span>Min Symbols</span>
              <span className="text-cyan-400 font-mono">{minSymbolCount}</span>
            </div>
            <input
              type="range"
              min={0}
              max={maxSymbols}
              step={1}
              value={minSymbolCount}
              onChange={(e) => setMinSymbolCount(Number(e.target.value))}
              className="accent-cyan-500 cursor-pointer h-1.5 bg-slate-700 rounded-lg appearance-none mt-1"
            />
          </div>

          {/* Language Select */}
          <div className="flex flex-col gap-1">
            <label className="text-xs font-medium text-slate-400">Language</label>
            <select
              value={selectedLang}
              onChange={(e) => setSelectedLang(e.target.value)}
              className="bg-slate-900 border border-slate-700 rounded px-2 py-1 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 transition-colors cursor-pointer"
            >
              {availableLanguages.map((lang) => (
                <option key={lang} value={lang}>
                  {lang}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Graph Visualizer / List View Area */}
      <div className="relative flex-1 min-h-[450px] p-4 bg-slate-950 overflow-auto">
        {filteredNodes.length === 0 ? (
          <div className="h-full w-full flex flex-col items-center justify-center text-slate-500 text-sm gap-2">
            <svg className="w-8 h-8 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            No nodes match the selected criteria. Try easing the filters.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {filteredNodes.map((node) => (
              <div
                key={node.id}
                onClick={() => onSelectNode && onSelectNode(node.id)}
                className="p-3 bg-slate-900/90 border border-slate-800 rounded-lg hover:border-cyan-500/50 hover:bg-slate-800/60 cursor-pointer transition-all flex flex-col justify-between gap-2 group"
              >
                <div className="truncate">
                  <p className="text-xs font-mono text-cyan-400 group-hover:text-cyan-300 truncate">
                    {node.name || node.id}
                  </p>
                  <p className="text-[10px] text-slate-500 font-mono truncate">{node.id}</p>
                </div>
                <div className="flex items-center justify-between text-[11px] text-slate-400 pt-2 border-t border-slate-800/80">
                  <span>{( (node.sizeBytes || 0) / 1024 ).toFixed(1)} KB</span>
                  <span>{node.symbolCount || 0} symbols</span>
                  {node.language && (
                    <span className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px]">
                      {node.language}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default DependencyGraph;