import os
from typing import Dict, List
import google.generativeai as genai

class CodebaseAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        else:
            self.model = None

    def explain_architecture(self, file_tree_summary: str, import_graph: Dict[str, List[str]]) -> str:
        """Generates an architectural synthesis based on static analysis data."""
        if not self.model:
            return "⚠️ GEMINI_API_KEY environment variable not found. Please set it to enable AI features."

        prompt = f"""
You are Forge, an elite software architecture analyzer.
Given the following repository structure and import graph, produce a concise architectural summary.

FILE HIERARCHY:
{file_tree_summary}

MODULE IMPORTS:
{import_graph}

Provide:
1. Core Architecture Pattern (e.g., Monorepo, Microservice, MVC)
2. Primary Component Roles
3. High-level Data Flow
"""
        response = self.model.generate_content(prompt)
        return response.text