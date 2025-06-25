# 1️⃣ Frontend build stage
FROM node:20 AS frontend
WORKDIR /app/client
COPY client/ .
RUN npm install && npm run build

# 2️⃣ Backend stage
FROM python:3.11-slim AS backend
RUN apt-get update && apt-get install -y build-essential && apt-get clean

WORKDIR /app

COPY backend/ ./backend
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Ensure static dir exists
RUN mkdir -p backend/app/static

# ✅ Copy frontend dist
COPY --from=frontend /app/client/dist ./backend/app/static

# Debug file presence
RUN ls -l ./backend/app/static/index.html || echo "⚠️ index.html missing"
RUN ls -l ./backend/app/static/assets || echo "⚠️ assets folder missing"

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/backend

# ✅ Use shell form for $PORT
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
