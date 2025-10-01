import asyncio
from typing import Any, Dict, List
from sqlalchemy import create_engine, inspect, text, exc

class SchemaDiscovery:
    """
    Connects to a database and discovers its schema, including tables,
    columns, and relationships.
    """
    def __init__(self, connection_string: str):
        if not connection_string:
            raise ValueError("Connection string cannot be empty.")
        self.connection_string = connection_string
        try:
            self.engine = create_engine(self.connection_string)
        except Exception as e:
            raise ConnectionError(f"Failed to create database engine: {e}")

    async def discover(self) -> Dict[str, Any]:
        """
        Asynchronously discovers the database schema.
        This is the public method to be called.
        """
        loop = asyncio.get_event_loop()
        try:
            # Use run_in_executor for the blocking database calls
            schema = await loop.run_in_executor(None, self._discover_schema_sync)
            return schema
        except exc.SQLAlchemyError as e:
            raise ConnectionError(f"Database connection error: {e}")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred during schema discovery: {e}")

    def _discover_schema_sync(self) -> Dict[str, Any]:
        """
        Synchronous method that performs the actual schema discovery.
        Should be run in a separate thread to avoid blocking the event loop.
        """
        with self.engine.connect() as connection:
            inspector = inspect(self.engine)
            tables_info = []
            schema_names = inspector.get_schema_names()
            
            for schema_name in schema_names:
                # We often want to ignore system schemas
                if schema_name not in ['information_schema', 'pg_catalog', 'sys']:
                    table_names = inspector.get_table_names(schema=schema_name)
                    for table_name in table_names:
                        columns = inspector.get_columns(table_name, schema=schema_name)
                        foreign_keys = inspector.get_foreign_keys(table_name, schema=schema_name)
                        
                        columns_info = [
                            {
                                "name": col["name"],
                                "type": str(col["type"]),
                                "primary_key": col.get("primary_key", False),
                                "nullable": col.get("nullable", True),
                            }
                            for col in columns
                        ]

                        relationships_info = [
                            {
                                "constrained_columns": fk["constrained_columns"],
                                "referred_table": fk["referred_table"],
                                "referred_columns": fk["referred_columns"],
                            }
                            for fk in foreign_keys
                        ]
                        
                        tables_info.append({
                            "name": table_name,
                            "columns": columns_info,
                            "relationships": relationships_info,
                        })

            return {"tables": tables_info}