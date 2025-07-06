# 1️⃣ Frontend build stage
FROM node:20 AS frontend

WORKDIR /app

# Copy frontend source
COPY client/ ./client

# Copy scripts used by frontend build (e.g., cache-bust)
COPY scripts/ ./scripts

# Install and build
RUN cd client && npm install && npm run build

# 2️⃣ Backend stage
FROM python:3.11-slim AS backend

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set base working directory
WORKDIR /app

# Copy backend source
COPY backend/ ./backend

# Copy Python requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Ensure static dir exists (just in case)
RUN mkdir -p backend/app/static

# Copy built frontend assets from the first stage
COPY --from=frontend /app/client/dist/ ./backend/app/static/

# Set working directory for FastAPI app
WORKDIR /app/backend

# Environment settings
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend

# Run FastAPI server (Heroku-compatible)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-5000}"]
