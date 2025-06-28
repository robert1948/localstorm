# 1️⃣ Frontend build stage
FROM node:20 AS frontend
WORKDIR /app/client
COPY client/ . 
RUN npm install && npm run build

# 2️⃣ Backend stage
FROM python:3.11-slim AS backend

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy backend source
COPY backend/ ./backend

# Copy Python requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure static dir exists
RUN mkdir -p backend/app/static

# Copy frontend build output into FastAPI static path
COPY --from=frontend /app/client/dist/ ./backend/app/static/

# Debug check (optional – remove in production for cleaner image)
RUN ls -l ./backend/app/static/index.html || echo "⚠️ index.html missing"
RUN ls -l ./backend/app/static/assets || echo "⚠️ assets folder missing"

# Environment setup
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend

# FastAPI startup
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
