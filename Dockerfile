# 1️⃣ Frontend build stage
FROM node:20 AS frontend
WORKDIR /app/client
COPY client/ .
RUN npm install && npm run build

# 2️⃣ Backend stage
FROM python:3.11-slim AS backend

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential && apt-get clean

# Set working directory
WORKDIR /app

# Copy backend source
COPY backend/ ./backend

# Copy Python requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create static directory if it doesn't exist
RUN mkdir -p backend/app/static

# Copy frontend build output into backend static dir
COPY --from=frontend /app/client/dist/ ./backend/app/static/

# Debug output: verify critical files copied correctly
RUN ls -l ./backend/app/static/index.html || echo "⚠️ index.html missing"
RUN ls -l ./backend/app/static/assets || echo "⚠️ assets folder missing"

# Environment config
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/backend

# Run FastAPI app using uvicorn
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]