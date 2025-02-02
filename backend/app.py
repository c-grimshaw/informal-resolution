from fastapi import FastAPI
from database import create_db_and_tables
from routes.auth import auth_router, users_router
from contextlib import asynccontextmanager
from models.user import UserCreate
from auth.users import get_user_manager, get_user_db
from fastapi_users.exceptions import UserAlreadyExists
from database import get_async_session
from fastapi.middleware.cors import CORSMiddleware
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
                email="admin@jsis.com",
                password="123",
                role="admin",
                is_superuser=True,
                is_active=True,
            ),
            is_system_init=True,
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

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend production server
        "http://localhost:5173",  # Frontend dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes
app.include_router(auth_router, prefix="/auth")
app.include_router(users_router, prefix="/users")
app.include_router(grievances.router)
