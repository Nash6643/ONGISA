from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class SymbolNode(BaseModel):
    name: str
    kind: str
    line_number: Optional[int] = None

class ImportNode(BaseModel):
    module: str
    name: Optional[str] = None
    alias: Optional[str] = None

class FileNode(BaseModel):
    path: str
    name: str
    extension: str
    size_bytes: int
    language: str
    symbols: List[SymbolNode] = []

class DependencyInfo(BaseModel):
    name: str
    version: Optional[str] = None

class RepositoryData(BaseModel):
    name: str
    files: List[FileNode] = []
    dependencies: List[DependencyInfo] = []
    languages: Dict[str, float] = {}

class HealthScoreReport(BaseModel):
    """Represents overall repository health and metric scores."""
    repository_name: str
    health_score: float
    maintainability_index: float
    total_smells: int
    severity_breakdown: Dict[str, int] = {}