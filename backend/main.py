import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# This is the crucial fix to ensure Python can find your modules.
# It adds the project's root directory to the Python path.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from .env file
load_dotenv()

from backend.api.routes import ingestion, query

app = FastAPI(
    title="AI-Powered NLP Query Engine",
    description="An API for querying databases and documents using natural language.",
    version="1.0.0",
)

# Add CORS middleware to allow all origins, which is necessary for the 
# frontend to communicate with the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for simplicity in this project
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the NLP Query Engine API!"}

# Include the API routers
app.include_router(ingestion.router, prefix="/api", tags=["Ingestion"])
# CORRECTED: The prefix is now consistent with the ingestion router.
app.include_router(query.router, prefix="/api", tags=["Query"])
