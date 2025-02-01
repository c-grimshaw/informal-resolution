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

# Create necessary directories
RUN mkdir -p /app/data && \
    mkdir -p /app/static/_app && \
    chown -R nobody:nogroup /app/data

# Copy backend files first
COPY backend/pyproject.toml ./
RUN pip install --no-cache-dir .
COPY backend/ .

# Copy frontend build to the correct location
COPY --from=frontend /frontend/build/index.html /app/static/
COPY --from=frontend /frontend/build/_app /app/static/_app

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"] 