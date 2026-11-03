import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({ health_score: 92.5, status: 'optimal' });
}