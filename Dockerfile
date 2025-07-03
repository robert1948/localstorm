# 1️⃣ Frontend build stage
FROM node:20 AS frontend
WORKDIR /app
COPY client/ ./client
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

# Copy Python requirements from root
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Ensure static dir exists
RUN mkdir -p backend/app/static

# Copy frontend build output into FastAPI static path
COPY --from=frontend /app/client/dist/ ./backend/app/static/

# Set working directory to where `app.main` lives
WORKDIR /app/backend

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend

# Start FastAPI (Heroku-compatible)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-5000}"]
