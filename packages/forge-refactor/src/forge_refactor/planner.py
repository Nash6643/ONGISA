"""
Automated Refactoring Planner for ONGISA.
Translates detected code smells into actionable, step-by-step refactoring plans.
"""

from typing import List, Dict, Any

class RefactorPlanner:
    """
    Stub planner for handling individual smell reports (e.g., Long Method splitting).
    """
    def plan_refactoring(self, smell_report: Dict[str, Any]) -> List[Dict[str, Any]]:
        plan = []
        smell_type = smell_report.get("smell") or smell_report.get("type")
        if smell_type == "LongMethod":
            plan.append({
                "action": "extract_method",
                "target_line": smell_report.get("line"),
                "status": "planned",
                "description": smell_report.get("message", "Method exceeds recommended length threshold."),
                "suggestion": "Extract cohesive segments of the long method into smaller helper functions."
            })
        return plan


class RefactoringPlanner:
    """
    Comprehensive automated refactoring planner for batch-translating multiple code smells.
    """
    def __init__(self, file_path: str, smells: List[Dict[str, Any]]):
        self.file_path = file_path
        self.smells = smells

    def generate_plan(self) -> Dict[str, Any]:
        steps = []
        for smell in self.smells:
            smell_type = smell.get("type") or smell.get("smell")
            line = smell.get("line", 0)
            message = smell.get("message", "")
            
            step = self._translate_smell_to_step(smell_type, line, message)
            if step:
                steps.append(step)

        return {
            "file_path": self.file_path,
            "total_smells": len(self.smells),
            "refactoring_steps": steps
        }

    def _translate_smell_to_step(self, smell_type: str, line: int, message: str) -> Dict[str, Any]:
        if smell_type == "LongMethod":
            return {
                "action": "EXTRACT_METHOD",
                "target_line": line,
                "description": f"Split long method: {message}",
                "suggestion": "Extract portions of this long method into smaller, dedicated helper methods."
            }
        elif smell_type == "DeepNesting":
            return {
                "action": "DECOMPOSE_CONDITIONAL_OR_EXTRACT",
                "target_line": line,
                "description": f"Refactor deep control flow nesting: {message}",
                "suggestion": "Extract inner blocks into private helper methods or use early returns (guard clauses) to reduce indentation depth."
            }
        elif smell_type == "LongParameterList":
            return {
                "action": "INTRODUCE_PARAMETER_OBJECT",
                "target_line": line,
                "description": f"Reduce parameter count: {message}",
                "suggestion": "Group related parameters into a dedicated data class, dataclass, or configuration object."
            }
        elif smell_type == "GodClass":
            return {
                "action": "EXTRACT_CLASS",
                "target_line": line,
                "description": f"Split oversized class responsibility: {message}",
                "suggestion": "Identify cohesive subsets of methods and state variables and extract them into separate cooperating service classes."
            }
        elif smell_type == "SyntaxError":
            return {
                "action": "FIX_SYNTAX",
                "target_line": line,
                "description": f"Resolve syntax error: {message}",
                "suggestion": "Correct the syntax error before running automated code transformations."
            }
        return None

def create_refactoring_plan(file_path: str, smells: List[Dict[str, Any]]) -> Dict[str, Any]:
    planner = RefactoringPlanner(file_path, smells)
    return planner.generate_plan()
