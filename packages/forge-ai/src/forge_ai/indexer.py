import os
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

class CodebaseVectorIndex:
    def __init__(self, collection_name: str = "forge_codebase"):
        # Load a fast local code/text embedding model
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(name=collection_name)

    def _get_embedding(self, text: str) -> List[float]:
        """Generate local vector embedding."""
        embedding = self.embedder.encode(text)
        return embedding.tolist()

    def index_files(self, file_contents: Dict[str, str]):
        """Chunk and insert codebase files into ChromaDB."""
        documents = []
        embeddings = []
        metadatas = []
        ids = []

        doc_id = 0
        for rel_path, content in file_contents.items():
            lines = content.split("\n")
            chunk_size = 50
            
            for i in range(0, len(lines), chunk_size):
                chunk = "\n".join(lines[i : i + chunk_size]).strip()
                if not chunk:
                    continue
                
                embedding = self._get_embedding(chunk)
                
                documents.append(chunk)
                embeddings.append(embedding)
                metadatas.append({
                    "file_path": rel_path,
                    "start_line": i + 1,
                    "end_line": min(i + chunk_size, len(lines))
                })
                ids.append(f"doc_{doc_id}")
                doc_id += 1

        if documents:
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve top_k most relevant code chunks for a user query."""
        query_embedding = self._get_embedding(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        retrieved_chunks = []
        if results and results["documents"]:
            for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
                retrieved_chunks.append({
                    "content": doc,
                    "file_path": meta["file_path"],
                    "start_line": meta["start_line"],
                    "end_line": meta["end_line"]
                })
        return retrieved_chunks