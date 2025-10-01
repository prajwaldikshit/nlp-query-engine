from typing import List, IO, Dict, Any
import PyPDF2
from docx import Document
from sentence_transformers import SentenceTransformer
import io

# In-memory storage for our document chunks and their embeddings.
# In a production system, this would be a proper vector database like Pinecone or ChromaDB.
document_store: List[Dict[str, Any]] = []

class DocumentProcessor:
    """
    Handles text extraction, chunking, and embedding generation for documents.
    """
    def __init__(self):
        # Using a small, efficient model for generating embeddings.
        # This model will be downloaded the first time it's used.
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    def _extract_text_from_pdf(self, file_content: bytes) -> str:
        """Extracts text from a PDF file's content."""
        reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    def _extract_text_from_docx(self, file_content: bytes) -> str:
        """Extracts text from a DOCX file's content."""
        doc = Document(io.BytesIO(file_content))
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    def _chunk_text(self, text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
        """Splits a long text into smaller, overlapping chunks based on words."""
        tokens = text.split()
        if not tokens:
            return []
        chunks = []
        for i in range(0, len(tokens), chunk_size - overlap):
            chunks.append(" ".join(tokens[i:i + chunk_size]))
        return chunks

    def process_documents(self, file_contents: List[bytes], filenames: List[str]) -> None:
        """
        Processes a list of uploaded files, generating and storing embeddings.
        """
        global document_store
        document_store.clear() # For this demo, we clear the store on each new upload.

        all_chunks = []
        for i, content in enumerate(file_contents):
            filename = filenames[i]
            text = ""
            if filename.lower().endswith(".pdf"):
                text = self._extract_text_from_pdf(content)
            elif filename.lower().endswith(".docx"):
                text = self._extract_text_from_docx(content)
            
            if text:
                chunks = self._chunk_text(text)
                for chunk in chunks:
                    all_chunks.append({"text": chunk, "filename": filename})
        
        if all_chunks:
            # Generate embeddings for all chunks in one batch for efficiency.
            chunk_texts = [item['text'] for item in all_chunks]
            embeddings = self.embedding_model.encode(chunk_texts)
            
            for i, item in enumerate(all_chunks):
                document_store.append({
                    "filename": item['filename'],
                    "chunk_text": item['text'],
                    "embedding": embeddings[i].tolist() # Convert numpy array to list for JSON
                })
