export interface GraphNode {
    id: string;
    label: string;
    extension: string;
    path: string;
  }
  
  export interface GraphEdge {
    source: string;
    target: string;
  }
  
  export interface AnalysisResult {
    status: string;
    filename: string;
    total_files: number;
    graph: {
      nodes: GraphNode[];
      edges: GraphEdge[];
    };
    issues: any[];
  }
  
  export async function uploadZipForAnalysis(file: File): Promise<AnalysisResult> {
    const formData = new FormData();
    formData.append("file", file);
  
    const response = await fetch("http://localhost:8000/api/analyze/zip", {
      method: "POST",
      body: formData,
    });
  
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Failed to analyze archive.");
    }
  
    return response.json();
  }