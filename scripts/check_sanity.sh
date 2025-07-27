#!/bin/bash

echo "🔍 Starting CapeControl sanity check..."
echo "========================================="

# 1. Check file structure
echo "📁 Project directory structure:"
tree -L 3 backend/

# 2. Check for syntax errors
echo -e "\n🧪 Checking Python syntax with compileall..."
python3 -m compileall backend/ || { echo "❌ Syntax errors found."; exit 1; }

# 3. Check for missing __init__.py files
echo -e "\n🔎 Looking for missing __init__.py files..."
missing_init=$(find backend/app -type d ! -path "*/__pycache__*" -exec test ! -f "{}/__init__.py" \; -print)

if [ -n "$missing_init" ]; then
  echo "❌ Missing __init__.py in:"
  echo "$missing_init"
else
  echo "✅ All directories have __init__.py"
fi

# 4. Lint with ruff (requires installation)
echo -e "\n🧹 Running ruff lint..."
if ! command -v ruff &> /dev/null; then
  echo "⚠️ Ruff not found. Install with: pip install ruff"
else
  ruff check backend/
fi

# 5. Environment variable check
echo -e "\n🌍 Checking for .env and required env vars..."
if [ -f ".env" ]; then
  echo "✅ .env file found"
else
  echo "⚠️ No .env file found"
fi

# Example critical env variable check
if grep -q "DATABASE_URL=" .env; then
  echo "✅ DATABASE_URL found"
else
  echo "⚠️ DATABASE_URL missing in .env"
fi

# 6. Uvicorn dry-run
echo -e "\n🚀 Starting FastAPI app in dry-run mode..."
UVICORN_COMMAND="uvicorn app.main:app --host 127.0.0.1 --port 8000 --app-dir backend/app"

if $UVICORN_COMMAND --lifespan off --loop asyncio --interface asgi3 --timeout-keep-alive 1 > /dev/null 2>&1 & then
  sleep 2
  kill $! >/dev/null 2>&1
  echo "✅ Uvicorn ran successfully"
else
  echo "❌ Uvicorn failed to run. Check app.main:app or dependencies."
fi

echo -e "\n✅ Sanity check completed."
echo "========================================="
