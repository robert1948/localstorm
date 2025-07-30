# Makefile for LocalStorm project

SCRIPT=./start_localstorm.sh
ENV ?= development

# Load .env file
ifneq ("$(wildcard .env)","")
	include .env
	export
endif

# ========== Commands ==========

dev:
	@echo "🔧 Starting LocalStorm (ENV=$(ENV))..."
	@chmod +x $(SCRIPT)
	@ENV=$(ENV) $(SCRIPT)

stop:
	@echo "🛑 Stopping LocalStorm processes..."
	@pkill -f "uvicorn backend.app.main:app" || true
	@pkill -f "vite" || true

clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf backend/__pycache__ backend/app/__pycache__ client/dist

build-frontend:
	@echo "🛠️  Building frontend with Vite..."
	cd client && npm install && npm run build
	@echo "☁️  Syncing static assets to S3..."
	@set -a && . .env && set +a && \
	aws s3 sync backend/app/static s3://$$AWS_BUCKET/$$AWS_PATH \
		--region $$AWS_REGION \
		--exclude "*" --include "*.png" --include "*.ico" --include "*.svg" --include "*.webmanifest" && \
	echo "✅ S3 sync completed: https://$$AWS_BUCKET.s3.$$AWS_REGION.amazonaws.com/$$AWS_PATH"

docker-build:
	docker-compose build

docker-up:
	@echo "🐳 Running Docker containers (ENV=$(ENV))..."
	@set -a && . .env && set +a && ENV=$(ENV) docker-compose up

docker-down:
	docker-compose down

s3-sync:
	@echo "☁️  Manually syncing static assets to S3..."
	@set -a && . .env && set +a && \
	aws s3 sync backend/app/static s3://$$AWS_BUCKET/$$AWS_PATH \
		--region $$AWS_REGION \
		--exclude "*" --include "*.png" --include "*.ico" --include "*.svg" --include "*.webmanifest" && \
	echo "✅ Manual S3 sync completed."

s3-list:
	@set -a && . .env && set +a && \
	aws s3 ls s3://$$AWS_BUCKET/$$AWS_PATH/ --region $$AWS_REGION

print-env:
	@echo "ENV=$(ENV)"
	@echo "AWS_BUCKET=$(AWS_BUCKET)"
	@echo "AWS_REGION=$(AWS_REGION)"
	@echo "AWS_PATH=$(AWS_PATH)"
