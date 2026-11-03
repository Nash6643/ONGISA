import os
import difflib
from typing import Dict, Any
from google import genai

class RefactorEngine:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required.")
        self.client = genai.Client(api_key=api_key)

    def generate_refactor_patch(self, file_path: str, file_content: str, instruction: str) -> Dict[str, Any]:
        """Generate a refactored version of the file content and return a unified diff patch."""
        prompt = (
            f"You are an expert software engineer and code refactoring specialist.\n"
            f"Refactor the following file according to the instructions provided.\n\n"
            f"### File: {file_path}\n"
            f"### Refactoring Instruction:\n"
            f"{instruction}\n\n"
            f"### Code:\n"
            f"```\n"
            f"{file_content}\n"
            f"```\n\n"
            f"### Response Format Rules:\n"
            f"Return ONLY the complete updated source code inside standard markdown code fences.\n"
            f"Do NOT include any preamble, conversational greeting, or explanations outside the code block."
        )

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        refactored_code = response.text.strip()
        if refactored_code.startswith("```"):
            lines = refactored_code.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            refactored_code = "\n".join(lines).strip()

        diff_lines = list(
            difflib.unified_diff(
                file_content.splitlines(keepends=True),
                refactored_code.splitlines(keepends=True),
                fromfile=f"a/{file_path}",
                tofile=f"b/{file_path}",
            )
        )
        diff_patch = "".join(diff_lines)

        return {
            "original_code": file_content,
            "refactored_code": refactored_code,
            "patch": diff_patch,
        }