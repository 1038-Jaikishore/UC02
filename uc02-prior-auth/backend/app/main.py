import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.authorizations import router as authorizations_router
from app.api.patients import router as patients_router
from app.api.llm import router as llm_router
from app.api.extractions import router as extractions_router
from app.api.policies import router as policies_router
from app.database.mongodb import db

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
app.include_router(patients_router)
app.include_router(llm_router)
app.include_router(extractions_router)
app.include_router(policies_router)

@app.on_event("startup")
async def startup_db_client():
    try:
        await db.connect_to_database()
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to connect to MongoDB on startup: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    await db.close_database_connection()

@app.get("/health")
async def health_check():
    mongo_connected = await db.is_connected()
    return {
        "status": "healthy" if mongo_connected else "degraded",
        "environment": os.getenv("ENV", "development"),
        "mongodb_connected": mongo_connected
    }
