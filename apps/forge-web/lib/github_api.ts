const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function analyzeGitHubRepository(repoUrl: string) {
  const response = await fetch(`${API_BASE_URL}/api/github/analyze-url`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ repo_url: repoUrl }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to ingest GitHub repository: ${errorText}`);
  }

  return response.json();
}