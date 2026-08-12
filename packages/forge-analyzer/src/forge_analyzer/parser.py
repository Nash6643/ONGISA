import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Node
from typing import List
from forge_core.schemas import SymbolInfo

class CodeParser:
    def __init__(self):
        # Initialize Python tree-sitter parser
        self.py_language = Language(tspython.language())
        self.parser = Parser(self.py_language)

    def parse_python_file(self, file_path: str, source_code: str) -> List[SymbolInfo]:
        """Scans a Python source file and extracts high-level AST symbols."""
        tree = self.parser.parse(bytes(source_code, "utf-8"))
        symbols: List[SymbolInfo] = []
        
        self._traverse_node(tree.root_node, file_path, symbols)
        return symbols

    def _traverse_node(self, node: Node, file_path: str, symbols: List[SymbolInfo]):
        """Recursively walks AST nodes to harvest functions and classes."""
        if node.type in ("function_definition", "class_definition"):
            name_node = node.child_by_field_name("name")
            symbol_name = name_node.text.decode("utf-8") if name_node else "anonymous"
            kind = "function" if node.type == "function_definition" else "class"
            
            symbols.append(
                SymbolInfo(
                    name=symbol_name,
                    kind=kind,
                    file_path=file_path,
                    line_start=node.start_point[0] + 1,
                    line_end=node.end_point[0] + 1,
                )
            )

        for child in node.children:
            self._traverse_node(child, file_path, symbols)