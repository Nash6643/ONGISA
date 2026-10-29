"""Rule to detect complex conditionals with excessive logical operators."""
from typing import Dict, Any, Optional

class ComplexConditionalDetector:
    def __init__(self, max_operators: int = 3):
        self.max_operators = max_operators

    def analyze_line(self, line_text: str, line_number: int) -> Optional[Dict[str, Any]]:
        ops = line_text.count(" and ") + line_text.count(" or ") + line_text.count("&&") + line_text.count("||")
        if ops > self.max_operators:
            return {
                "smell": "ComplexConditional",
                "severity": "warning",
                "line": line_number,
                "message": f"Conditional has {ops} logical operators (exceeds threshold of {self.max_operators})."
            }
        return None