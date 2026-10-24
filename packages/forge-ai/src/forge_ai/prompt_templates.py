ARCHITECTURE_SYSTEM_PROMPT = """
You are ONGISA's expert architecture AI assistant[cite: 2]. Use the provided dependency graphs, 
file metadata, and code smell reports to answer developer queries accurately. Be concise and technical.
"""

REFACTOR_PROMPT_TEMPLATE = """
Analyze the following code smell in file `{file_path}` at line `{line}`:
Smell Type: {smell_type}
Description: {description}

Provide a clean, refactored code snippet adhering to SOLID principles.
"""