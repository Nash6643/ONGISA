import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { source_code, file_path } = body;

    // Basic heuristic/parser or call to your Python backend service
    // For demonstration, we'll extract function declarations and calls to build nodes & edges
    const nodes: { id: string; label: string; type: string }[] = [];
    const edges: { source: string; target: string }[] = [];

    if (source_code) {
      const lines = source_code.split('\n');
      lines.forEach((line: string, idx: number) => {
        // Match function declarations (e.g., function name, const name = ...)
        const funcMatch = line.match(/(?:function\s+([a-zA-Z0-9_]+))|(?:const\s+([a-zA-Z0-9_]+)\s*=\s*(?:async\s*)?\()/);
        if (funcMatch) {
          const funcName = funcMatch[1] || funcMatch[2];
          nodes.push({
            id: funcName,
            label: `${funcName} (line ${idx + 1})`,
            type: 'function',
          });
        }
      });

      // If we found functions, create mock or detected call edges between them
      if (nodes.length > 1) {
        for (let i = 0; i < nodes.length - 1; i++) {
          edges.push({
            source: nodes[i].id,
            target: nodes[i + 1].id,
          });
        }
      }
    }

    return NextResponse.json({
      success: true,
      graph: {
        nodes,
        edges,
      },
    });
  } catch (error: any) {
    return NextResponse.json(
      { success: false, error: error.message || 'Failed to generate call graph' },
      { status: 500 }
    );
  }
}