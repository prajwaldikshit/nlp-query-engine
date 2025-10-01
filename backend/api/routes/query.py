from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
import sqlalchemy

from backend.services.query_engine import QueryEngine
from backend.services.query_cache import QueryCache

router = APIRouter()
query_engine = QueryEngine()
query_cache = QueryCache()

class QueryRequest(BaseModel):
    user_query: str
    db_schema: Dict[str, Any]
    connection_string: str # We now need this to execute the query

@router.post("/query")
async def process_query(request: QueryRequest):
    """
    Processes a user's natural language query.
    1. Checks the cache for a previous result.
    2. If not found, generates a SQL query using the AI.
    3. Executes the SQL query against the database.
    4. Caches the result and returns it.
    """
    # Create a unique key for caching based on the query and connection
    cache_key = f"{request.connection_string}:{request.user_query.lower().strip()}"
    cached_result = query_cache.get(cache_key)

    if cached_result:
        return {"message": "Result from cache", "data": cached_result, "query_type": "SQL"}

    # Step 2: Generate the SQL query
    generated_sql = query_engine.generate_sql(request.user_query, request.db_schema)

    if generated_sql.startswith("Error:"):
        raise HTTPException(status_code=400, detail=generated_sql)

    # Step 3: Execute the generated SQL query
    try:
        engine = sqlalchemy.create_engine(request.connection_string)
        with engine.connect() as connection:
            result = connection.execute(sqlalchemy.text(generated_sql))
            
            # Convert the result to a list of dictionaries to be JSON-friendly
            if result.returns_rows:
                # For queries like SELECT *, SELECT name, etc.
                data = [dict(row) for row in result.mappings()]
            else:
                # For queries like COUNT(*), the value is in the first column of the first row
                # .scalar() fetches this single value
                data = [{"result": result.scalar()}]

            # Step 4: Cache the new result
            query_cache.set(cache_key, data)

            return {"message": "SQL query executed successfully", "data": data, "generated_sql": generated_sql, "query_type": "SQL"}
    except Exception as e:
        print(f"SQL execution error: {e}")
        raise HTTPException(status_code=500, detail=f"Error executing SQL query: {str(e)}")