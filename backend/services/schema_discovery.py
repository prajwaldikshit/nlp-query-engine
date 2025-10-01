import sqlalchemy as db
from typing import Any, Dict, List

class SchemaDiscovery:
    """
    Connects to a database and discovers its schema, including tables,
    columns, and relationships.
    """
    def __init__(self, connection_string: str):
        """
        Initializes the discovery service with the database connection string.
        """
        if not connection_string:
            raise ValueError("Connection string cannot be empty.")
        self.connection_string = connection_string
        self.engine = db.create_engine(self.connection_string)
        self.metadata = db.MetaData()

    def discover(self) -> Dict[str, Any]:
        """
        Performs the schema discovery.
        This is a synchronous method.
        """
        try:
            # The reflect method inspects the database and populates the metadata object
            self.metadata.reflect(bind=self.engine)
            
            schema_info = {"tables": []}
            
            for table_name, table in self.metadata.tables.items():
                table_info = {
                    "name": table_name,
                    "columns": [],
                    "relationships": []
                }
                
                # Get columns and their types
                for column in table.columns:
                    table_info["columns"].append({
                        "name": column.name,
                        "type": str(column.type),
                        "primary_key": column.primary_key,
                        "nullable": column.nullable,
                    })

                # Get foreign key relationships
                for fk in table.foreign_keys:
                    table_info["relationships"].append({
                        "constrained_columns": [c.name for c in fk.constraint.columns],
                        "referred_table": fk.column.table.name,
                        "referred_columns": [fk.column.name]
                    })
                
                schema_info["tables"].append(table_info)
                
            return schema_info
        except Exception as e:
            # In case of an error (e.g., bad connection string), re-raise it
            raise Exception(f"Failed to discover schema: {e}")