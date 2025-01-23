from fastapi import FastAPI
from database import create_db_and_tables
from routes.auth import auth_router, users_router
from contextlib import asynccontextmanager
from models.user import UserCreate
from auth.users import get_user_manager, get_user_db
from fastapi_users.exceptions import UserAlreadyExists
from database import get_async_session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from routes import grievances

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    
    # Create admin user if it doesn't exist
    try:
        # Get database session
        async_session_generator = get_async_session()
        session = await anext(async_session_generator)
        
        # Get user_db
        user_db_generator = get_user_db(session)
        user_db = await anext(user_db_generator)
        
        # Get user manager
        user_manager_generator = get_user_manager(user_db)
        user_manager = await anext(user_manager_generator)
        
        await user_manager.create(
            UserCreate(
                email="admin@example.com",
                password="123",
                role="admin",
                is_superuser=True,
                is_active=True
            ),
            is_system_init=True
        )
        print("Admin user created successfully")
    except UserAlreadyExists:
        print("Admin user already exists")
    except Exception as e:
        print(f"Error creating admin user: {e}")
    finally:
        await session.close()
    
    yield

app = FastAPI(lifespan=lifespan)

# Simplified CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth")
app.include_router(users_router, prefix="/users")
app.include_router(grievances.router)

# Mount frontend static files
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

# Serve index.html for all unmatched routes (SPA fallback)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    return FileResponse(os.path.join(frontend_path, "index.html"))
