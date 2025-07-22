#!/bin/bash

# Heroku PostgreSQL Migration Script for Email Verification
# Run this script from your local machine where you have internet access

echo "🚀 Heroku PostgreSQL Migration for Email Verification"
echo "=================================================="

# Database connection details
DATABASE_URL="postgresql://u8h1en29mru00:p3020c7560854b178b598d2993a2b91173972e98a202f19c9ba981e3bbd8@c7jla3ha5puqsf.cluster-czrs8kj4isg6.us-east-1.rds.amazonaws.com:5432/d5h1tdp6nrlcj8"

echo "🔍 Checking if verification_codes table exists..."

# Check if table exists
TABLE_EXISTS=$(psql "$DATABASE_URL" -t -c "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'verification_codes');" 2>/dev/null | xargs)

if [ "$TABLE_EXISTS" = "t" ]; then
    echo "⚠️  verification_codes table already exists"
    echo "🔍 Checking table structure..."
    psql "$DATABASE_URL" -c "\\d verification_codes"
    exit 0
fi

echo "📋 Creating verification_codes table..."

# Create the verification_codes table
psql "$DATABASE_URL" -c "
CREATE TABLE verification_codes (
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
    echo "✅ Created verification_codes table"
else
    echo "❌ Failed to create verification_codes table"
    exit 1
fi

echo "🔍 Creating database indexes..."

# Create indexes
psql "$DATABASE_URL" -c "
CREATE INDEX idx_verification_codes_email ON verification_codes (email);
CREATE INDEX idx_verification_codes_active ON verification_codes (email, purpose, is_used, expires_at);
"

if [ $? -eq 0 ]; then
    echo "✅ Created database indexes"
else
    echo "❌ Failed to create indexes"
    exit 1
fi

echo "🔍 Verifying table structure..."
psql "$DATABASE_URL" -c "\\d verification_codes"

echo ""
echo "✅ Migration completed successfully!"
echo "🎉 Email verification system is now ready on Heroku PostgreSQL"
