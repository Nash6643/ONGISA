import { NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

export async function GET() {
  const encoder = new TextEncoder();
  const projectRoot = path.resolve(process.cwd(), '..', '..');

  const stream = new ReadableStream({
    start(controller) {
      const child = spawn(
        'python',
        ['CLI/forge-cli/src/forge_cli/main.py', 'analyze', '.'],
        {
          cwd: projectRoot,
          env: {
            ...process.env,
            PYTHONPATH:
              'packages/forge-refactor/src;packages/forge-analyzer/src;packages/forge-core/src;packages/forge-ai/src',
          },
        }
      );

      child.stdout.on('data', (data) => {
        controller.enqueue(encoder.encode(`data: ${data.toString()}\n\n`));
      });

      child.stderr.on('data', (data) => {
        controller.enqueue(encoder.encode(`data: [stderr] ${data.toString()}\n\n`));
      });

      child.on('close', () => {
        controller.enqueue(encoder.encode('data: [DONE]\n\n'));
        controller.close();
      });
    },
  });

  return new NextResponse(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      Connection: 'keep-alive',
    },
  });
}