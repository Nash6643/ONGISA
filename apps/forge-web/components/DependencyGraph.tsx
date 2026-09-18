'use client';

import React, { useMemo, useState } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  Node,
  Edge,
  useNodesState,
  useEdgesState,
  MarkerType,
} from 'reactflow';
import 'reactflow/dist/style.css';

interface GraphDataProps {
  initialNodes?: Array<{ id: string; label: string; extension: string; path: string }>;
  initialEdges?: Array<{ source: string; target: string }>;
}

export default function DependencyGraph({ initialNodes = [], initialEdges = [] }: GraphDataProps) {
  const [selectedNode, setSelectedNode] = useState<any | null>(null);

  // Convert raw API graph data into React Flow nodes with grid layout
  const formattedNodes: Node[] = useMemo(() => {
    if (!initialNodes.length) {
      // Fallback demo topology nodes if no zip is loaded yet
      return [
        { id: '1', data: { label: 'forge_ai/main.py' }, position: { x: 250, y: 50 }, style: { background: '#0f172a', color: '#38bdf8', border: '1px solid #0284c7', borderRadius: '8px', padding: '10px' } },
        { id: '2', data: { label: 'forge_core/zip_handler.py' }, position: { x: 100, y: 200 }, style: { background: '#0f172a', color: '#34d399', border: '1px solid #059669', borderRadius: '8px', padding: '10px' } },
        { id: '3', data: { label: 'forge_analyzer/parser.py' }, position: { x: 400, y: 200 }, style: { background: '#0f172a', color: '#a78bfa', border: '1px solid #7c3aed', borderRadius: '8px', padding: '10px' } },
      ];
    }

    const cols = Math.ceil(Math.sqrt(initialNodes.length));
    return initialNodes.map((n, idx) => ({
      id: n.id,
      data: { label: n.label, path: n.path, extension: n.extension },
      position: {
        x: (idx % cols) * 220 + 50,
        y: Math.floor(idx / cols) * 120 + 50,
      },
      style: {
        background: '#090d16',
        color: '#f3f4f6',
        border: '1px solid #1f2937',
        borderRadius: '8px',
        fontSize: '12px',
        padding: '8px 12px',
        width: 180,
      },
    }));
  }, [initialNodes]);

  const formattedEdges: Edge[] = useMemo(() => {
    if (!initialEdges.length) {
      return [
        { id: 'e1-2', source: '1', target: '2', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
        { id: 'e1-3', source: '1', target: '3', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
      ];
    }

    return initialEdges.map((e, idx) => ({
      id: `e-${idx}`,
      source: e.source,
      target: e.target,
      animated: true,
      style: { stroke: '#0284c7', strokeWidth: 1.5 },
      markerEnd: { type: MarkerType.ArrowClosed, color: '#0284c7' },
    }));
  }, [initialEdges]);

  const [nodes, , onNodesChange] = useNodesState(formattedNodes);
  const [edges, , onEdgesChange] = useEdgesState(formattedEdges);

  const handleNodeClick = (_: React.MouseEvent, node: Node) => {
    setSelectedNode(node);
  };

  return (
    <div className="flex gap-4 h-[600px] w-full">
      <div className="flex-1 bg-gray-950 border border-gray-800 rounded-xl overflow-hidden relative">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={handleNodeClick}
          fitView
        >
          <Background color="#1e293b" gap={16} />
          <Controls className="bg-gray-900 border-gray-800 text-white fill-white" />
          <MiniMap nodeColor="#0284c7" maskColor="rgba(15, 23, 42, 0.7)" className="bg-gray-900 border-gray-800" />
        </ReactFlow>
      </div>

      {/* Selected Node Details Drawer */}
      <div className="w-80 bg-gray-900 border border-gray-800 rounded-xl p-4 flex flex-col justify-between">
        <div>
          <h3 className="text-sm font-semibold text-cyan-400 uppercase tracking-wider mb-3">
            Node Inspector
          </h3>
          {selectedNode ? (
            <div className="space-y-3 font-mono text-xs">
              <div>
                <span className="text-gray-500 block">Identifier:</span>
                <span className="text-gray-200 break-all">{selectedNode.id}</span>
              </div>
              <div>
                <span className="text-gray-500 block">File Name:</span>
                <span className="text-gray-200">{selectedNode.data.label}</span>
              </div>
              {selectedNode.data.path && (
                <div>
                  <span className="text-gray-500 block">Relative Path:</span>
                  <span className="text-gray-200 break-all">{selectedNode.data.path}</span>
                </div>
              )}
            </div>
          ) : (
            <p className="text-xs text-gray-500 italic">
              Click any node on the canvas to inspect file relationships and dependency properties.
            </p>
          )}
        </div>

        <div className="pt-4 border-t border-gray-800">
          <p className="text-[10px] text-gray-500 uppercase tracking-widest">
            ONGISA Graph Engine v0.1.0
          </p>
        </div>
      </div>
    </div>
  );
}