import os
from google import genai


class CodebaseAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is missing."
            )

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"

    def explain_architecture(
        self,
        file_tree: str,
        imports: dict,
    ) -> str:

        prompt = f"""
You are Forge AI, an expert software architecture assistant.

Analyze this repository and explain its architecture.

### File Tree
{file_tree}

### Import Graph
{imports}

Provide a concise architectural analysis covering:

1. Overall Architecture
2. Major Components
3. Component Responsibilities
4. Dependency Relationships
5. High-Level Data Flow
6. Potential Architectural Problems

Do not invent files, dependencies, or behavior that are not supported
by the provided repository information.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text

    def answer_with_rag(
        self,
        query: str,
        relevant_chunks: list,
    ) -> str:

        context = "\n\n".join(
            f"""--- File: {c['file_path']}
Lines: {c['start_line']}-{c['end_line']}
{c['content']}
"""
            for c in relevant_chunks
        )

        prompt = f"""
You are Forge AI, an expert software architecture assistant.

Answer the developer's question using ONLY the relevant code
provided below.

### Relevant Code Context
{context}

### Developer Question
{query}

Rules:

- Ground your answer in the provided code.
- Do not invent files, functions, dependencies, or behavior.
- If the provided context is insufficient, explicitly say so.
- Explain the reasoning clearly.
- Give practical recommendations when appropriate.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text

    def query_architecture(
        self,
        question: str,
        codebase_context: dict,
    ) -> str:

        prompt = f"""
You are Forge AI, an expert software architecture assistant.

Analyze the repository information below and answer the developer's
question.

### Codebase Context
{codebase_context}

### Developer Question
{question}

Focus on:

- architecture
- dependencies
- data flow
- code organization
- code smells
- potential refactoring
- technical tradeoffs

Only make claims supported by the provided repository information.
If the context is insufficient, say what information is missing.

Provide a concise, technical, actionable response.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text