import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.authorizations import router as authorizations_router

load_dotenv()

app = FastAPI(title="UC02 - Prior Authorization Triage & Policy Companion API")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(authorizations_router)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": os.getenv("ENV", "development"),
        "mongodb_connected": False  # Handled in Phase 3
    }
