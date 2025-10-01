# AI-Powered NLP Query Engine

This project is a full-stack web application that serves as an intelligent, natural language query engine for an employee database. It can connect to any SQL database, automatically discover its schema, and answer questions posed in plain English by generating and executing SQL queries. It can also ingest and prepare unstructured documents (like PDFs and DOCX files) for future searching.
This project was built as a submission for the AI Engineering internship assignment.
---
## Core Features:

Dynamic Schema Discovery: Automatically discovers the schema (tables, columns, relationships) of any connected SQL database without hard-coding.

Natural Language to SQL: Utilizes Google's Gemini Pro AI model to translate natural language questions into executable SQL queries.

SQL Execution & Caching: The backend not only generates but also executes the SQL query against the database. A caching mechanism is implemented to provide instant results for repeated queries, demonstrating performance optimization.

Document Processing: An endpoint is available to upload and process unstructured documents (.pdf, .docx), preparing them for semantic search by extracting text.

Full-Stack Interface: A clean, modern web interface built with HTML, Tailwind CSS, and vanilla JavaScript allows users to interact with all backend features seamlessly.

---
## Tech Stack:

Backend: Python 3, FastAPI, SQLAlchemy, Uvicorn

AI Model: Google Gemini Pro

Database: SQLite (for demo), compatible with PostgreSQL/MySQL

Document Processing: PyPDF2, python-docx

Frontend: HTML, Tailwind CSS, Vanilla JavaScript

---
## Project Structure:

nlp-query-engine/
+-- backend/
¦   +-- api/
¦   ¦   +-- routes/
¦   ¦       +-- ingestion.py
¦   ¦       +-- query.py
¦   +-- services/
¦       +-- document_processor.py
¦       +-- query_cache.py
¦       +-- query_engine.py
¦       +-- schema_discovery.py
+-- frontend/
¦   +-- index.html
+-- .env
+-- create_test_db.py
+-- populate_db.py
+-- README.md
+-- requirements.txt

---

## Setup and Installation
Follow these steps to set up and run the project locally.

### Prerequisites:
- Python 3.8+
- A Git client

1. Clone the Repository
   
git clone [https://github.com/your-username/nlp-query-engine.git](https://github.com/your-username/nlp-query-engine.git)
cd nlp-query-engine

2. Set Up The Backend
   
a. Create and Activate Virtual Environment:
# Create the virtual environment
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows (Git Bash)
source venv/Scripts/activate

b. Install Dependencies:
pip install -r requirements.txt

c. Set Up Environment Variables:
Create a .env file in the root directory of the project and add your Google Gemini API key.

GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE"


d. Create and Populate the Database:

Run the following scripts in order to create the database schema and fill it with sample data.

# First, create the database tables
python create_test_db.py

# Second, populate the tables with data
python populate_db.py

---

3. Run the Application
   
a. Start the Backend Server:

With your virtual environment active, run the following command from the root project directory:
python -m uvicorn backend.main:app --reload
The server will be running at http://127.0.0.1:8000.

b. Launch the Frontend:

Navigate to the frontend/ directory and open the index.html file in your web browser.

You can now interact with the application!

---
## Screenshots:
<img width="1919" height="868" alt="image" src="https://github.com/user-attachments/assets/a6a89eb5-2e43-4727-815b-9325b70297e2" />
<img width="1919" height="865" alt="image" src="https://github.com/user-attachments/assets/98f6f61b-d23b-4913-aa8a-12c02be6e530" />


