#!/bin/bash

# Heroku Database Migration via Heroku CLI
# Run this script to migrate the Heroku PostgreSQL database

echo "🚀 Running Heroku PostgreSQL Migration for Email Verification"
echo "============================================================="

# Get the Heroku app name (replace with your actual app name)
APP_NAME="cape-control-app"  # Update this to match your Heroku app name

echo "📱 Heroku App: $APP_NAME"
echo "🗄️  Connecting to Heroku PostgreSQL..."

# Check if Heroku CLI is available
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if user is logged in
if ! heroku auth:whoami &> /dev/null; then
    echo "❌ Please login to Heroku first: heroku login"
    exit 1
fi

# Run the migration SQL directly via Heroku CLI
echo "📋 Creating verification_codes table..."

heroku pg:psql --app $APP_NAME --command "
CREATE TABLE IF NOT EXISTS verification_codes (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    code VARCHAR(6) NOT NULL,
    purpose VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    used_at TIMESTAMP NULL,
    is_used BOOLEAN DEFAULT FALSE,
    attempts INTEGER DEFAULT 0,
    user_agent TEXT NULL,
    ip_address VARCHAR(45) NULL
);
"

if [ $? -eq 0 ]; then
    echo "✅ verification_codes table created successfully"
else
    echo "❌ Failed to create verification_codes table"
    exit 1
fi

echo "🔍 Creating database indexes..."

heroku pg:psql --app $APP_NAME --command "
CREATE INDEX IF NOT EXISTS idx_verification_codes_email 
ON verification_codes (email);

CREATE INDEX IF NOT EXISTS idx_verification_codes_active 
ON verification_codes (email, purpose, is_used, expires_at);
"

if [ $? -eq 0 ]; then
    echo "✅ Database indexes created successfully"
else
    echo "❌ Failed to create database indexes"
    exit 1
fi

echo "🔍 Verifying table structure..."

heroku pg:psql --app $APP_NAME --command "\d verification_codes"

echo ""
echo "✅ Migration completed successfully!"
echo "🎉 Email verification system is now ready on Heroku!"
echo ""
echo "📊 Next steps:"
echo "  1. Test the email verification API endpoints"
echo "  2. Integrate frontend email verification flow"
echo "  3. Configure email service settings"
