"""Rule to detect deeply nested code blocks."""
from typing import Dict, Any, Optional

class DeepNestingDetector:
    def __init__(self, max_depth: int = 4):
        self.max_depth = max_depth

    def analyze_indentation(self, indent_level: int, line_number: int) -> Optional[Dict[str, Any]]:
        if indent_level > self.max_depth:
            return {
                "smell": "DeepNesting",
                "severity": "warning",
                "line": line_number,
                "message": f"Nesting depth of {indent_level} exceeds maximum allowed depth of {self.max_depth}."
            }
        return None