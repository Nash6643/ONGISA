import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import path from 'path';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { targetFile, rule } = body;

    const projectRoot = path.resolve(process.cwd(), '..', '..');
    const cmd = `python CLI/forge-cli/src/forge_cli/main.py refactor ${targetFile || '.'} --dry-run`;

    return new Promise((resolve) => {
      exec(
        cmd,
        {
          cwd: projectRoot,
          env: {
            ...process.env,
            PYTHONPATH: 'packages/forge-refactor/src;packages/forge-analyzer/src;packages/forge-core/src;packages/forge-ai/src',
          },
        },
        (error, stdout, stderr) => {
          if (error) {
            resolve(NextResponse.json({ error: stderr || error.message }, { status: 500 }));
            return;
          }
          resolve(NextResponse.json({ status: 'success', output: stdout }));
        }
      );
    });
  } catch (err) {
    return NextResponse.json({ error: 'Failed to execute refactoring task' }, { status: 500 });
  }
}