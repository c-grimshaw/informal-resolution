# Build frontend
FROM node:20-slim AS frontend
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Build backend
FROM python:3.13-rc-slim
WORKDIR /app

# Create src directory and copy Python package files
RUN mkdir -p /app/src
WORKDIR /app/src
COPY backend/pyproject.toml backend/app.py backend/database.py ./
COPY backend/auth ./auth
COPY backend/models ./models
COPY backend/routes ./routes
COPY backend/schemas ./schemas

# Install dependencies
WORKDIR /app
RUN pip install --no-cache-dir -e src/

# Create necessary directories and copy scripts
RUN mkdir -p data && \
    chown -R nobody:nogroup data && \
    chmod 777 data
COPY backend/scripts ./scripts

# Set Python path to include src directory
ENV PYTHONPATH=/app/src

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"] 