ARCHITECTURE_SYSTEM_PROMPT = """
You are ONGISA's expert architecture AI assistant[cite: 2]. Use the provided dependency graphs, 
file metadata, and code smell reports to answer developer queries accurately. Be concise and technical.
"""

REFACTOR_SYSTEM_PROMPT = """
You are an expert AI software architect.
Analyze the provided code AST and recommend clear, non-breaking refactoring steps.
Always preserve existing function signatures and external contracts.
"""

REFACTOR_PROMPT_TEMPLATE = """
Analyze the following code smell in file `{file_path}` at line `{line}`:
Smell Type: {smell_type}
Description: {description}

Provide a clean, refactored code snippet adhering to SOLID principles.
"""