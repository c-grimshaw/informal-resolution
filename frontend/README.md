# NOI - Notice of Intent System

A grievance management system built for CANSOFCOM, using SvelteKit for the frontend and FastAPI for the backend.

## Project Structure

```
.
├── frontend/         # SvelteKit frontend application
├── backend/         # FastAPI backend application
└── docker-compose.yml
```

## Development Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   # Frontend
   cd frontend
   npm install

   # Backend
   cd ../backend
   pip install -e .
   ```

3. Run in development mode:
   ```bash
   # Frontend
   cd frontend
   npm run dev

   # Backend (in a separate terminal)
   cd backend
   uvicorn app:app --reload
   ```

## Docker Deployment

The entire application can be run using Docker Compose:

```bash
docker compose up --build
```

This will:
1. Build the frontend static files
2. Start the FastAPI backend server
3. Populate test data automatically
4. Make the application available at http://localhost:8000

## Features

- User authentication and authorization
- Grievance submission and tracking
- Unit-based access control
- Kanban board for grievance management
- Analytics and reporting
- Mobile-responsive design

## Test Data

The system automatically populates test data on startup, including:
- Supervisors for each unit
- Sample grievances with various statuses
- Random notes and updates

## Tech Stack

- Frontend:
  - SvelteKit
  - Chart.js for analytics
  - Lucide icons
  - Modern CSS with responsive design

- Backend:
  - FastAPI
  - SQLite database
  - FastAPI Users for authentication
  - SQLAlchemy ORM
