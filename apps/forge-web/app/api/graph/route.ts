import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET() {
  try {
    const graphPath = path.join(process.cwd(), '..', '..', 'graph.json');
    if (!fs.existsSync(graphPath)) {
      return NextResponse.json({ error: 'graph.json not found. Run analysis first.' }, { status: 404 });
    }

    const fileData = fs.readFileSync(graphPath, 'utf8');
    const graphData = JSON.parse(fileData);
    return NextResponse.json(graphData);
  } catch (error) {
    return NextResponse.json({ error: 'Failed to read graph data' }, { status: 500 });
  }
}