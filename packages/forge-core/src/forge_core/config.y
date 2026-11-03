from pydantic import BaseModel, Field

class ForgeConfig(BaseModel):
    project_name: str = Field(..., description="Name of the analyzed repository")
    max_line_length: int = Field(default=120, description="Threshold for line length smells")
    ignore_patterns: list[str] = Field(default_factory=lambda: ["node_modules", ".git", "venv"])