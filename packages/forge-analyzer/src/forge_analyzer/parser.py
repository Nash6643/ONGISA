from tree_sitter import Language, Parser
import tree_sitter_python as tspython
import tree_sitter_typescript as tstypescript
import tree_sitter_rust as tsrust
from typing import List, Tuple
from forge_core.schemas import SymbolNode, ImportNode

class CodeParser:
    def __init__(self):
        self.py_parser = Parser(Language(tspython.language()))
        self.ts_parser = Parser(Language(tstypescript.language_typescript()))
        self.tsx_parser = Parser(Language(tstypescript.language_tsx()))
        self.rs_parser = Parser(Language(tsrust.language()))

    def parse_python_file(self, file_path: str, content: str) -> Tuple[List[SymbolNode], List[ImportNode]]:
        tree = self.py_parser.parse(bytes(content, "utf-8"))
        symbols = []
        imports = []

        query_str = """
            (function_definition name: (identifier) @func.name) @func.def
            (class_definition name: (identifier) @class.name) @class.def
            (import_statement) @imp
            (import_from_statement) @imp_from
        """
        query = Language(tspython.language()).query(query_str)
        captures = query.captures(tree.root_node)

        for node, tag in captures:
            if tag in ["func.name", "class.name"]:
                symbols.append(
                    SymbolNode(
                        name=node.text.decode("utf-8"),
                        kind="function" if tag == "func.name" else "class",
                        line_number=node.start_point[0] + 1
                    )
                )
            elif tag in ["imp", "imp_from"]:
                imports.append(
                    ImportNode(
                        module=node.text.decode("utf-8").strip(),
                        imported_symbols=[]
                    )
                )

        return symbols, imports

    def parse_typescript_file(self, file_path: str, content: str, is_tsx: bool = False) -> Tuple[List[SymbolNode], List[ImportNode]]:
        lang = Language(tstypescript.language_tsx() if is_tsx else tstypescript.language_typescript())
        parser = self.tsx_parser if is_tsx else self.ts_parser
        tree = parser.parse(bytes(content, "utf-8"))
        symbols = []
        imports = []

        query_str = """
            (function_declaration name: (identifier) @func.name)
            (class_declaration name: (type_identifier) @class.name)
            (interface_declaration name: (type_identifier) @interface.name)
            (import_statement) @imp
        """
        query = lang.query(query_str)
        captures = query.captures(tree.root_node)

        for node, tag in captures:
            if tag in ["func.name", "class.name", "interface.name"]:
                kind = "function" if tag == "func.name" else ("class" if tag == "class.name" else "interface")
                symbols.append(
                    SymbolNode(
                        name=node.text.decode("utf-8"),
                        kind=kind,
                        line_number=node.start_point[0] + 1
                    )
                )
            elif tag == "imp":
                imports.append(
                    ImportNode(
                        module=node.text.decode("utf-8").strip(),
                        imported_symbols=[]
                    )
                )

        return symbols, imports

    def parse_rust_file(self, file_path: str, content: str) -> Tuple[List[SymbolNode], List[ImportNode]]:
        tree = self.rs_parser.parse(bytes(content, "utf-8"))
        symbols = []
        imports = []

        query_str = """
            (function_item name: (identifier) @func.name)
            (struct_item name: (type_identifier) @struct.name)
            (enum_item name: (type_identifier) @enum.name)
            (use_declaration) @use
        """
        query = Language(tsrust.language()).query(query_str)
        captures = query.captures(tree.root_node)

        for node, tag in captures:
            if tag in ["func.name", "struct.name", "enum.name"]:
                kind = "function" if tag == "func.name" else ("struct" if tag == "struct.name" else "enum")
                symbols.append(
                    SymbolNode(
                        name=node.text.decode("utf-8"),
                        kind=kind,
                        line_number=node.start_point[0] + 1
                    )
                )
            elif tag == "use":
                imports.append(
                    ImportNode(
                        module=node.text.decode("utf-8").strip(),
                        imported_symbols=[]
                    )
                )

        return symbols, imports