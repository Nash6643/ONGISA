from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class SymbolInfo(BaseModel):
    name: str
    kind: str  # 'function', 'class', 'method', 'import'
    file_path: str
    line_start: int
    line_end: int
    docstring: Optional[str] = None

class DependencyInfo(BaseModel):
    name: str
    version: Optional[str] = None
    is_vulnerable: bool = False
    vulnerability_details: Optional[str] = None

class FileNode(BaseModel):
    path: str
    name: str
    extension: str
    size_bytes: int
    language: Optional[str] = None
    symbols: List[SymbolInfo] = Field(default_factory=list)

class RepositoryData(BaseModel):
    url_or_path: str
    languages: Dict[str, float]  # e.g. {"Python": 80.5, "TypeScript": 19.5}
    files: List[FileNode]
    dependencies: List[DependencyInfo]