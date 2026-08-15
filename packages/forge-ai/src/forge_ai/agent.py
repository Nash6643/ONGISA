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

    def start_chat_session(self, file_tree: str, imports: dict):
        system_instruction = f"""
You are Forge AI, an expert software architecture assistant.
You have indexed the user's codebase with the following details:

### File Tree
{file_tree}

### Import Graph
{imports}

Answer developer questions specifically using this context. Be concise, precise, and practical.
"""
        return self.client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
            ),
        )