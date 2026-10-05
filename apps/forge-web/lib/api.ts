/**
 * Frontend API Client for ONGISA Web Dashboard.
 * Handles communication with the forge-api backend service.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface SmellAnalysisRequest {
  file_path: string;
  source_code: string;
}

export interface SmellItem {
  type: string;
  message: string;
  line: number;
  severity: 'low' | 'medium' | 'high';
}

export interface RefactoringStep {
  action: string;
  target_line: number;
  description: string;
  suggestion: string;
}

export interface SmellAnalysisResponse {
  file_path: string;
  smells: SmellItem[];
  refactoring_plan: {
    file_path: string;
    total_smells: number;
    refactoring_steps: RefactoringStep[];
  };
}

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

  return response.json();
}