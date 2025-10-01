from pydantic import BaseModel, Field

class ConnectionRequest(BaseModel):
    """
    Pydantic model for the database connection request body.
    Ensures the incoming JSON has the correct format.
    """
    connection_string: str = Field(
        ..., 
        example="sqlite:///./test.db",
        description="The connection string for the database (e.g., PostgreSQL, SQLite)."
    )