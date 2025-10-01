from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile

# Corrected absolute imports
from backend.models.database import ConnectionRequest
from backend.services.document_processor import DocumentProcessor
from backend.services.schema_discovery import SchemaDiscovery

router = APIRouter()


@router.post("/connect-database")
def connect_database(request: ConnectionRequest):
    """
    Connects to a database, discovers its schema, and returns it.
    This is a synchronous endpoint.
    """
    try:
        discovery_service = SchemaDiscovery(request.connection_string)
        schema = discovery_service.discover() # Calling the synchronous method
        if not schema or not schema.get("tables"):
            raise HTTPException(
                status_code=404, detail="Could not find any tables in the database."
            )
        return {"message": "Database schema discovered successfully!", "schema": schema}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database connection failed: {e}"
        )


@router.post("/upload-documents")
def upload_documents(files: List[UploadFile] = File(...)):
    """
    Receives and processes uploaded document files.
    This is a synchronous endpoint, which is more robust for file I/O.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files were uploaded.")
    try:
        processor = DocumentProcessor()
        processor.process_documents(files)
        return {"message": f"{len(files)} documents processed and indexed successfully."}
    except ValueError as ve:
         raise HTTPException(status_code=400, detail=f"An error occurred during document processing: {ve}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred during document processing: {e}"
        )