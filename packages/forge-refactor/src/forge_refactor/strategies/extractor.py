class MethodExtractorStrategy:
    @staticmethod
    def suggest_extraction(function_name: str, target_lines: tuple[int, int]) -> dict:
        return {
            "strategy": "extract_method",
            "target_function": function_name,
            "line_range": target_lines,
            "suggestion": "Extract inner block into a dedicated private helper method."
        }