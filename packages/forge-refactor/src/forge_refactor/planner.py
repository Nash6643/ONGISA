import os
import google.generativeai as genai

class RefactoringPlanner:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY", "")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    def generate_refactoring_plan(self, file_path: str, code_content: str, issue_description: str) -> str:
        if not self.model:
            return "Gemini API key not configured for refactoring planning."

        prompt = f"""
        You are ONGISA's Expert Refactoring Architect. Analyze the following target file and its detected architectural smell, then provide a safe, step-by-step refactoring transformation plan.

        File Path: {file_path}
        Detected Issue: {issue_description}

        Source Code Snippet:
        {code_content[:2000]}

        Provide:
        1. An architectural explanation of why this is an issue.
        2. Proposed modular breakdown (e.g., separating responsibilities).
        3. A dry-run preview of proposed file changes or new file paths.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating refactoring plan: {str(e)}"