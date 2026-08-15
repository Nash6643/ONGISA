import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Node
from typing import List, Tuple
from forge_core.schemas import SymbolInfo

class CodeParser:
    def __init__(self):
        self.py_language = Language(tspython.language())
        self.parser = Parser(self.py_language)

    def parse_python_file(self, file_path: str, source_code: str) -> Tuple[List[SymbolInfo], List[str]]:
        """Scans a Python file for AST symbols and imported modules."""
        tree = self.parser.parse(bytes(source_code, "utf-8"))
        symbols: List[SymbolInfo] = []
        imports: List[str] = []
        
        self._traverse_node(tree.root_node, file_path, symbols, imports)
        return symbols, imports

    def _traverse_node(self, node: Node, file_path: str, symbols: List[SymbolInfo], imports: List[str]):
        # Extract Functions & Classes
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

        # Extract Import Statements
        elif node.type in ("import_statement", "import_from_statement"):
            raw_import = node.text.decode("utf-8").strip()
            imports.append(raw_import)

        for child in node.children:
            self._traverse_node(child, file_path, symbols, imports)