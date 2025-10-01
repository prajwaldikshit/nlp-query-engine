from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Corrected absolute imports
from backend.services.document_processor import DocumentProcessor
from backend.services.query_cache import QueryCache
from backend.services.query_engine import QueryEngine
import sqlalchemy


class QueryRequest(BaseModel):
    user_query: str
    db_schema: Dict[str, Any]
    connection_string: str


router = APIRouter()
query_engine = QueryEngine()
query_cache = QueryCache()
# Get the singleton instance of the document processor
document_processor = DocumentProcessor()


def classify_query(user_query: str) -> str:
    """
    A simple keyword-based classifier to determine the query type.
    """
    doc_keywords = ["resume", "skills", "contract", "clause", "document", "file", "pdf"]
    if any(keyword in user_query.lower() for keyword in doc_keywords):
        return "DOCUMENT"
    return "SQL"


# CORRECTED: The path is now explicitly defined here.
@router.post("/query")
def process_query(request: QueryRequest):
    """
    Processes a natural language query by classifying it, executing it, and returning the result.
    """
    user_query = request.user_query
    cache_key = f"{user_query}_{request.connection_string}"

    # Check cache first
    cached_result = query_cache.get(cache_key)
    if cached_result:
        return {
            "message": "Result from cache",
            "data": cached_result["data"],
            "query_type": cached_result["query_type"],
        }

    query_type = classify_query(user_query)

    if query_type == "SQL":
        try:
            # Generate and execute SQL query
            generated_sql = query_engine.generate_sql(user_query, request.db_schema)
            if generated_sql.startswith("Error"):
                raise HTTPException(status_code=400, detail=generated_sql)

            engine = sqlalchemy.create_engine(request.connection_string)
            with engine.connect() as connection:
                result = connection.execute(sqlalchemy.text(generated_sql))
                data = [row._asdict() for row in result]

            response = {
                "message": "SQL query executed successfully",
                "data": data,
                "generated_sql": generated_sql,
                "query_type": "SQL",
            }
            query_cache.set(cache_key, response)
            return response

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"An error occurred during SQL processing: {e}"
            )

    elif query_type == "DOCUMENT":
        try:
            # Perform document search
            search_results = document_processor.search_documents(user_query)
            response = {
                "message": "Document search executed successfully",
                "data": search_results,
                "query_type": "DOCUMENT",
            }
            # We can also cache document results
            query_cache.set(cache_key, response)
            return response
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred during document search: {e}",
            )

    raise HTTPException(status_code=400, detail="Could not classify the query.")