from typing import AsyncGenerator
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Check if we're running in Docker by checking for the /app directory
IS_DOCKER = os.path.exists('/app')

# Use different database paths for Docker vs local development
if IS_DOCKER:
    DEFAULT_DB_URL = "sqlite+aiosqlite:////app/data/test.db"
else:
    # Use a local path in the backend directory
    BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(BACKEND_DIR, 'data'), exist_ok=True)
    DEFAULT_DB_URL = f"sqlite+aiosqlite:///{os.path.join(BACKEND_DIR, 'data', 'test.db')}"

DATABASE_URL = os.getenv('DATABASE_URL', DEFAULT_DB_URL)

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session 