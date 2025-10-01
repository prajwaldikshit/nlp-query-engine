import io
from typing import List, Dict, Any
import docx
import PyPDF2
from sentence_transformers import SentenceTransformer, util

# Use a smaller, faster model for this project.
# This model will be downloaded automatically the first time it's used.
model = SentenceTransformer('all-MiniLM-L6-v2')

class DocumentProcessor:
    """
    A singleton class to handle document processing, chunking, embedding generation,
    and in-memory storage.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DocumentProcessor, cls).__new__(cls)
            cls._instance.chunks = []
            cls._instance.embeddings = None
            print("DocumentProcessor initialized.")
        return cls._instance

    def process_documents(self, files: List[Any]) -> int:
        """
        Processes a list of uploaded files, extracts text, chunks, and creates embeddings.
        """
        self.chunks = []
        all_texts = []
        for file in files:
            content = file.file.read()
            if file.filename.endswith(".pdf"):
                text = self._read_pdf(content)
            elif file.filename.endswith(".docx"):
                text = self._read_docx(content)
            else:
                continue
            
            if text:
                # Simple chunking by paragraph
                all_texts.extend(text.split('\n\n'))

        self.chunks = [chunk for chunk in all_texts if chunk.strip()]
        if self.chunks:
            self.embeddings = model.encode(self.chunks, convert_to_tensor=True)
        
        return len(self.chunks)

    def search_documents(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Searches the indexed documents for a given query.
        """
        if not self.chunks or self.embeddings is None:
            return []

        query_embedding = model.encode(query, convert_to_tensor=True)
        
        # Use semantic search to find the most relevant chunks
        hits = util.semantic_search(query_embedding, self.embeddings, top_k=top_k)
        
        # 'hits' is a list of lists, we take the first list for the first query
        hits = hits[0]
        
        search_results = []
        for hit in hits:
            # THE FIX: Convert the numpy float score to a standard Python float
            # before adding it to the results.
            search_results.append({
                'chunk': self.chunks[hit['corpus_id']],
                'score': float(hit['score']) 
            })
            
        return search_results

    def _read_pdf(self, content: bytes) -> str:
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(content))
            return "".join(page.extract_text() for page in reader.pages)
        except Exception:
            return ""

    def _read_docx(self, content: bytes) -> str:
        try:
            doc = docx.Document(io.BytesIO(content))
            return "\n\n".join(para.text for para in doc.paragraphs)
        except Exception:
            return ""
