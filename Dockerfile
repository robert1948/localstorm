# 1️⃣ Frontend build stage
FROM node:20 AS frontend

WORKDIR /app

# Copy frontend source and scripts
COPY client/ ./client
COPY scripts/ ./scripts

# Let scripts know we're inside Docker to avoid local-only actions
ENV INSIDE_DOCKER=true

# Install dependencies and build
RUN cd client && npm install && npm run build
RUN node scripts/cache-bust.cjs

# 2️⃣ Backend stage
FROM python:3.11-slim AS backend

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy backend source and requirements
COPY backend/ ./backend
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Ensure static dir exists
RUN mkdir -p backend/app/static

# Copy built frontend assets from previous stage
COPY --from=frontend /app/client/dist/ ./backend/app/static/

# Set FastAPI working directory
WORKDIR /app/backend

# Environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend

# Launch FastAPI
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-5000}"]
