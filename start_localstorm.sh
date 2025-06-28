#!/bin/bash

# Define ports
BACKEND_PORT=8000
FRONTEND_PORT=3000

# Function to free a port
free_port() {
  local port=$1
  echo "🔄 Checking port $port..."
  pids=$(lsof -ti :$port)
  if [[ -n "$pids" ]]; then
    echo "🔌 Port $port in use by PIDs: $pids. Killing..."
    kill -9 $pids
    echo "✅ Port $port freed."
  else
    echo "✅ Port $port already free."
  fi
}

# Free required ports
free_port $BACKEND_PORT
free_port $FRONTEND_PORT

# Trap cleanup on exit
cleanup() {
  echo "🧹 Cleaning up..."
  pkill -f "uvicorn backend.app.main:app"
  pkill -f "vite"
}
trap cleanup EXIT

# Start backend
echo "🚀 Starting backend on http://localhost:$BACKEND_PORT ..."
uvicorn backend.app.main:app --reload --port $BACKEND_PORT &
BACKEND_PID=$!

# Start frontend
echo "🚀 Starting frontend on http://localhost:$FRONTEND_PORT ..."
cd client && npm run dev -- --port $FRONTEND_PORT &
FRONTEND_PID=$!
cd ..

# Wait briefly
sleep 2

# Show access URLs
echo -e "\n✅ Access URLs:"
echo "🔹 Backend:  http://localhost:$BACKEND_PORT"
echo "🔹 Frontend: http://localhost:$FRONTEND_PORT"

# Wait for both background processes to exit
wait $BACKEND_PID
wait $FRONTEND_PID
