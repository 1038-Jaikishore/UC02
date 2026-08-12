import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

    async def connect_to_database(self):
        mongodb_uri = os.getenv("MONGODB_URI")
        db_name = os.getenv("DATABASE_NAME", "prior_auth_db")

        if not mongodb_uri:
            logger.error("MONGODB_URI is not configured.")
            self.client = None
            self.db = None
            return

        try:
            logger.info("Attempting to connect to MongoDB Atlas...")
            # Set short timeout parameters so we don't block indefinitely on failures
            self.client = AsyncIOMotorClient(
                mongodb_uri,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000
            )
            self.db = self.client[db_name]
            # Ping the admin database to verify connectivity
            await self.client.admin.command("ping")
            logger.info("MongoDB connection verified successfully.")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            self.client = None
            self.db = None
            raise e

    async def is_connected(self) -> bool:
        if not self.client:
            return False
        try:
            await self.client.admin.command("ping")
            return True
        except Exception:
            return False

    async def close_database_connection(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")

db = MongoDB()

async def get_database():
    if db.db is None or db.client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection is currently unavailable"
        )
    return db.db
