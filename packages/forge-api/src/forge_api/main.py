import os
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from forge_core.zip_handler import extract_zip_archive
from forge_core.schemas import FileNode
from forge_analyzer import (
    CodeParser,
    DependencyGraph,
    DependencyAnalyzer,
    MultiLangParser,
    ArchitectureDetector,
)

app = FastAPI(title="ONGISA API Engine")

# Enable CORS for local Next.js frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/analyze/zip")
async def analyze_zip_upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip files are supported.")

    # Save uploaded file bytes to a temporary zip file on disk
    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_zip_path = tmp_file.name

    extracted_dir = None
    try:
        # Extract archive using core handler
        extracted_dir = extract_zip_archive(tmp_zip_path)
        
        ts_parser = MultiLangParser()
        fallback_parser = CodeParser()
        dep_graph = DependencyGraph()
        files_data = []

        # Traverse extracted directory
        for root, dirs, files in os.walk(extracted_dir):
            dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", "node_modules", ".venv", "venv"}]
            for f in files:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, extracted_dir)
                ext = os.path.splitext(f)[1].lower()

                files_data.append(
                    FileNode(
                        path=rel_path,
                        name=f,
                        extension=ext,
                        size_bytes=os.path.getsize(full_path),
                        language="Supported" if ext in [".py", ".ts", ".tsx", ".js", ".rs", ".java", ".go"] else "Other",
                        symbols=[]
                    )
                )

        # Run architectural detection
        issues = []
        issues.extend(ArchitectureDetector.detect_god_modules(files_data))
        issues.extend(ArchitectureDetector.detect_orphan_modules(files_data, dep_graph))

        return {
            "status": "success",
            "filename": file.filename,
            "total_files": len(files_data),
            "issues": [issue.dict() for issue in issues]
        }

    finally:
        # Cleanup temporary zip and extracted files
        if os.path.exists(tmp_zip_path):
            os.remove(tmp_zip_path)
        if extracted_dir and os.path.exists(extracted_dir):
            shutil.rmtree(extracted_dir)