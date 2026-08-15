import os
from google import genai

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

Provide a concise high-level architectural overview.
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text