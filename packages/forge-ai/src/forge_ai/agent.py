import os
from google import genai
from google.genai import types

class CodebaseAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is missing.")
        self.client = genai.Client(api_key=api_key)

    def explain_architecture(self, file_tree: str, imports: dict) -> str:
        prompt = f"""
Analyze the following codebase structure and import graph:

### File Tree
{file_tree}

### Imports
{imports}

Provide a concise high-level architectural overview covering:
1. Overall Architecture
2. Primary Component Roles
3. High-level Data Flow
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text

    def answer_with_rag(self, query: str, relevant_chunks: list) -> str:
        """Answer user questions grounded in retrieved code snippets."""
        context = "\n\n".join(
            f"--- File: {c['file_path']} (Lines {c['start_line']}-{c['end_line']}) ---\n{c['content']}"
            for c in relevant_chunks
        )

        prompt = f"""
You are Forge AI, an expert software architecture assistant.
Answer the developer's question using the relevant codebase snippets below:

### Relevant Code Context
{context}

### Question
{query}

Provide a precise, concise, and practical explanation.
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text