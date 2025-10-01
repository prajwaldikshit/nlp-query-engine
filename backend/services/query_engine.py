import os
import google.generativeai as genai

class QueryEngine:
    """
    Handles the logic for processing natural language queries using the Gemini API.
    """
    def __init__(self):
        try:
            # This configures the library with your API key.
            genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
            # Use the standard, stable 'gemini-pro' model.
            self.model = genai.GenerativeModel('models/gemini-2.5-pro')
        except KeyError:
            # This error is raised if the API key isn't found in the environment.
            raise ValueError("GOOGLE_API_KEY not found. Please ensure it's in your .env file and loaded in main.py.")

    def _construct_prompt(self, user_query: str, db_schema: dict) -> str:
        """Constructs a detailed prompt for the AI to generate a SQL query."""
        
        schema_str = ""
        # Loop through each table in the schema provided by the user.
        for table in db_schema.get('tables', []):
            # Add table name and column names to the prompt string.
            schema_str += f"Table '{table['name']}' has columns: {', '.join(col['name'] for col in table['columns'])}.\n"
            # Add information about relationships (foreign keys).
            for rel in table.get('relationships', []):
                schema_str += f"  - Relationship: '{table['name']}.{rel['constrained_columns'][0]}' is a foreign key to '{rel['referred_table']}.{rel['referred_columns'][0]}'.\n"

        # The final prompt template that will be sent to the AI.
        prompt = f"""
        Given the following database schema:
        ---
        {schema_str}
        ---
        Based on this schema, write a single, valid SQLite SQL query to answer the following user question.
        Only return the SQL query and nothing else. Do not wrap it in markdown.

        User Question: "{user_query}"
        SQL Query:
        """
        return prompt

    def generate_sql(self, user_query: str, db_schema: dict) -> str:
        """
        Generates a SQL query from a natural language user query.
        """
        if not user_query:
            return "Error: Query cannot be empty."

        # Build the full prompt.
        prompt = self._construct_prompt(user_query, db_schema)

        try:
            # Send the prompt to the Gemini API.
            response = self.model.generate_content(prompt)
            # Clean up the response to get just the SQL.
            generated_sql = response.text.strip().replace('`', '')
            
            # A basic security check to ensure only SELECT queries are generated.
            if not generated_sql.upper().strip().startswith("SELECT"):
                return "Error: Generated query was not a valid SELECT statement."

            return generated_sql

        except Exception as e:
            # If anything goes wrong with the API call, print the error and return a generic message.
            print(f"An error occurred while calling the Gemini API: {e}")
            return "Error: Could not generate SQL query due to an API issue."