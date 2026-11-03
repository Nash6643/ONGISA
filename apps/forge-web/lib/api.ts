/**
 * Frontend API Client for ONGISA Web Dashboard.
 * Handles communication with the forge-api backend service.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface SmellAnalysisRequest {
  file_path: string;
  source_code: string;
}

export interface RefactorApplyRequest {
  file_path: string;
  source_code: string;
  steps: RefactoringStep[];
}

export interface RefactorApplyResponse {
  success: boolean;
  file_path: string;
  original_code: string;
  refactored_code: string;
  message: string;
}

export async function applyRefactoringPatch(payload: RefactorApplyRequest): Promise<RefactorApplyResponse> {
  const response = await fetch(`${API_BASE_URL}/api/refactor/apply`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to apply refactoring patch: ${errorText}`);
  }

  return response.json();
}

export interface SmellItem {
  type: string;
  message: string;
  description?: string;
  line: number;
  severity: 'low' | 'medium' | 'high';
}

export async function fetchCallGraph(sourceCode: string, filePath: string) {
  const response = await fetch('/api/graph', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ source_code: sourceCode, file_path: filePath }),
  });

  if (!response.ok) {
    throw new Error('Failed to fetch call graph');
  }

  const data = await response.json();
  return data.graph;
}

export interface RefactoringStep {
  action: string;
  target_line: number;
  description: string;
  suggestion: string;
}

export interface GraphNode {
  id: string;
  label: string;
  type?: string;
}

export interface GraphEdge {
  source: string;
  target: string;
}

export interface AnalysisResult {
  file_path?: string;
  smells?: SmellItem[];
  issues?: SmellItem[];
  graph?: {
    nodes: GraphNode[];
    edges: GraphEdge[];
  };
  refactoring_plan?: {
    file_path: string;
    total_smells: number;
    refactoring_steps: RefactoringStep[];
  };
}

export type SmellAnalysisResponse = AnalysisResult;

/**
 * Sends source code to the backend for smell detection and refactoring plan generation.
 */
export async function analyzeCodeSmells(payload: SmellAnalysisRequest): Promise<SmellAnalysisResponse> {
  const response = await fetch(`${API_BASE_URL}/api/analyze/smells`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to analyze code smells: ${errorText}`);
  }

  const data = await response.json();
  
  data.graph = data.graph || { nodes: [], edges: [] };
  if (data.smells) {
    data.smells = data.smells.map((s: SmellItem) => ({
      ...s,
      description: s.description || s.message,
    }));
    data.issues = data.smells;
  } else {
    data.issues = data.issues || [];
  }

  return data;
}

export async function analyzeRepositoryZip(zipFile: File): Promise<AnalysisResult> {
  const formData = new FormData();
  formData.append('file', zipFile);

  const response = await fetch(`${API_BASE_URL}/api/analyze/zip`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to analyze repository zip: ${errorText}`);
  }

  return response.json();
}