import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const aiServiceUrl = process.env.FORGE_AI_URL || 'http://127.0.0.1:8000';
    
    const response = await fetch(`${aiServiceUrl}/api/chat/architecture`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      throw new Error(`AI Service responded with status ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (err: any) {
    return NextResponse.json(
      { error: err.message || 'Failed to query architecture assistant' },
      { status: 500 }
    );
  }
}