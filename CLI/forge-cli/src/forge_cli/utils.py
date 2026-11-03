import sys

def exit_with_code(smell_count: int, strict: bool = False):
    if smell_count > 0 and strict:
        sys.exit(1)
    sys.exit(0)
