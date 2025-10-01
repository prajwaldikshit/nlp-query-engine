from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import asyncio

from backend.services.schema_discovery import SchemaDiscovery
from backend.services.document_processor import DocumentProcessor
from pydantic import BaseModel

router = APIRouter()

class DBConnection(BaseModel):
    connection_string: str

# In-memory storage for simplicity. In a real app, use a proper vector DB.
document_store = {
    "chunks": [],
    "embeddings": None
}

@router.post("/connect-database")
async def connect_database(db_info: DBConnection):
    """
    Connects to a database and discovers its schema.
    """
    try:
        # Step 1: Create the SchemaDiscovery object with the connection string.
        schema_discoverer = SchemaDiscovery(connection_string=db_info.connection_string)
        
        # Step 2: Call the discover() method to get the schema.
        schema = await schema_discoverer.discover()
        
        if not schema or not schema.get("tables"):
            raise HTTPException(status_code=404, detail="No tables found in the database.")

        return {"message": "Database schema discovered successfully!", "schema": schema}
    except Exception as e:
        # Provide a more specific error message back to the frontend
        error_message = f"Database connection failed: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)


@router.post("/upload-documents")
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Accepts multiple document uploads, processes them, and stores embeddings.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files were uploaded.")

    processor = DocumentProcessor()
    
    try:
        # Process all files concurrently
        contents = await asyncio.gather(*[file.read() for file in files])
        filenames = [file.filename for file in files]
        
        all_chunks = await processor.process_documents(contents, filenames)
        
        if not all_chunks:
            raise HTTPException(status_code=500, detail="Failed to extract any text from the documents.")

        document_store["chunks"] = all_chunks
        
        return {"message": f"{len(files)} documents processed and indexed successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during document processing: {str(e)}")

