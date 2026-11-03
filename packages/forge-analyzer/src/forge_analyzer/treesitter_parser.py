from typing import List, Dict, Any
from tree_sitter import Language, Parser
import tree_sitter_python as tspython
import tree_sitter_javascript as tsjavascript
import tree_sitter_typescript as tstypescript
import tree_sitter_rust as tsrust
import tree_sitter_go as tsgo

from forge_core.schemas import SymbolNode, ImportNode

class MultiLangParser:
    def __init__(self):
        self.languages = {
            "python": Language(tspython.language()),
            "javascript": Language(tsjavascript.language()),
            "typescript": Language(tstypescript.language_typescript()),
            "tsx": Language(tstypescript.language_tsx()),
            "rust": Language(tsrust.language()),
            "go": Language(tsgo.language()),
        }
        self.parser = Parser()

    def parse_code(self, code: str, lang_key: str) -> Dict[str, Any]:
        """Parse source code into AST symbols and import dependencies."""
        if lang_key not in self.languages:
            return {"symbols": [], "imports": []}

        language = self.languages[lang_key]
        self.parser.set_language(language)
        tree = self.parser.parse(bytes(code, "utf-8"))
        
        symbols = []
        imports = []
        
        root_node = tree.root_node
        self._traverse(root_node, code, lang_key, symbols, imports)

        return {"symbols": symbols, "imports": imports}

    def _traverse(self, node, code: str, lang_key: str, symbols: List[SymbolNode], imports: List[ImportNode]):
        """Recursively traverse AST nodes to extract functions, classes, and imports."""
        node_type = node.type

        # Function / Method definitions
        if node_type in {"function_definition", "function_declaration", "method_definition", "function_item"}:
            name_node = node.child_by_field_name("name")
            if name_node:
                symbol_name = code[name_node.start_byte:name_node.end_byte]
                symbols.append(
                    SymbolNode(
                        name=symbol_name,
                        kind="function",
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1
                    )
                )

        # Class / Struct / Interface definitions
        elif node_type in {"class_definition", "class_declaration", "struct_item", "interface_declaration", "type_spec"}:
            name_node = node.child_by_field_name("name")
            if name_node:
                symbol_name = code[name_node.start_byte:name_node.end_byte]
                symbols.append(
                    SymbolNode(
                        name=symbol_name,
                        kind="class",
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1
                    )
                )

        # Imports / Uses / Includes
        elif "import" in node_type or node_type in {"use_declaration", "import_statement", "import_spec"}:
            import_text = code[node.start_byte:node.end_byte].strip()
            imports.append(
                ImportNode(
                    module=import_text,
                    line_number=node.start_point[0] + 1
                )
            )

        for child in node.children:
            self._traverse(child, code, lang_key, symbols, imports)