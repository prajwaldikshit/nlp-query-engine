import sys
import os

# --- START OF FIX ---
# This block forces the application to see the libraries inside your venv
# It resolves the stubborn "ModuleNotFoundError"
venv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'venv'))
site_packages = os.path.join(venv_path, 'Lib', 'site-packages')
if site_packages not in sys.path:
    sys.path.insert(0, site_packages)
# --- END OF FIX ---

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import ingestion, query

# Load environment variables from the .env file in the project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

app = FastAPI(
    title="NLP Query Engine API",
    description="API for the Natural Language Query Engine for Employee Data.",
    version="1.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for simplicity, can be restricted
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include API routers
app.include_router(ingestion.router, prefix="/api", tags=["Data Ingestion"])
app.include_router(query.router, prefix="/api", tags=["Query Processing"])

@app.get("/", tags=["Root"])
async def read_root():
    """
    A welcome message to verify that the API is running.
    """
    return {"message": "Welcome to the NLP Query Engine API!"}