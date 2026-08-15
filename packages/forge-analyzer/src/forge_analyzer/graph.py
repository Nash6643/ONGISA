from typing import Dict, List, Set
from pydantic import BaseModel, Field

class SymbolNode(BaseModel):
    id: str  # e.g. "forge_core.cloner.WorkspaceManager"
    file_path: str
    symbol_name: str
    kind: str
    calls: Set[str] = Field(default_factory=set)

class DependencyGraph(BaseModel):
    nodes: Dict[str, SymbolNode] = Field(default_factory=dict)
    imports: Dict[str, List[str]] = Field(default_factory=dict)  # file_path -> list of imported modules

    def add_import(self, file_path: str, imported_module: str):
        if file_path not in self.imports:
            self.imports[file_path] = []
        if imported_module not in self.imports[file_path]:
            self.imports[file_path].append(imported_module)

    def add_symbol(self, symbol_node: SymbolNode):
        self.nodes[symbol_node.id] = symbol_node