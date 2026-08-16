import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET() {
  try {
    // Go up two levels from apps/forge-web to reach C:\Users\Omar\Desktop\forge\graph.json
    const graphPath = path.resolve(process.cwd(), '..', '..', 'graph.json');

    if (!fs.existsSync(graphPath)) {
      return NextResponse.json(
        { error: `graph.json not found at ${graphPath}. Run CLI analysis first.` },
        { status: 404 }
      );
    }

    const fileData = fs.readFileSync(graphPath, 'utf8');
    const graphData = JSON.parse(fileData);
    return NextResponse.json(graphData);
  } catch (error) {
    return NextResponse.json({ error: 'Failed to read graph data' }, { status: 500 });
  }
}